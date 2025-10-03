import logging
import os
import sys

import httpx
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryPushNotifier, InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from app.agent import KaitlynAgent
from app.agent_executor import KaitlynAgentExecutor
from dotenv import load_dotenv

#Server that will be hosting Kaitlyn's Agent.
#Contains the request_handler, which will be what will handle the request from the host agent.
#Contains the agent_card, which will be what will allow the host agent to know what Kaitlyn's Agent can do.
#Contains the agent_executor, which will be what will bridge the gap between our agent's invoke / kickoff / etc. that actually triggers the agent (the way we trigger the agent would differ between frameworks), and is a crucial standardization step in A2A.
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


def main():
    """Starts Kaitlyn's Agent server."""
    host = "localhost"
    port = 10004
    try:
        if not os.getenv("GOOGLE_API_KEY"):
            raise MissingAPIKeyError("GOOGLE_API_KEY environment variable not set.")

        capabilities = AgentCapabilities(streaming=True, pushNotifications=True)
        skill = AgentSkill(
            id="schedule_pickleball",
            name="Pickleball Scheduling Tool",
            description="Helps with finding Kaitlyn's availability for pickleball",
            tags=["scheduling", "pickleball"],
            examples=["Are you free to play pickleball on Saturday?"],
        )
        agent_card = AgentCard(
            name="Kaitlynn Agent",
            description="Helps with scheduling pickleball games",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            defaultInputModes=KaitlynAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=KaitlynAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

        httpx_client = httpx.AsyncClient()
        # In this request handler, we will be including our push notifier, which will be what will allow the host agent to know that Kaitlyn's Agent is ready to receive a request.
        # That is, we're sending the notification to the host agent from the server instead of the host agent reaching out to the server.
        request_handler = DefaultRequestHandler(
            agent_executor=KaitlynAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_notifier=InMemoryPushNotifier(httpx_client),
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        uvicorn.run(server.build(), host=host, port=port)

    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
