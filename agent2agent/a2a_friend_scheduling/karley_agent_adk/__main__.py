import logging
import os

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent import create_agent
from agent_executor import KarleyAgentExecutor
from dotenv import load_dotenv
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

#This file is the actual server that will be hosting Karley's Agent.
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""

    pass


def main():
    """Starts the agent server."""
    host = "localhost"
    port = 10002
    try:
        # Check for API key only if Vertex AI is not configured
        if not os.getenv("GOOGLE_GENAI_USE_VERTEXAI") == "TRUE":
            if not os.getenv("GOOGLE_API_KEY"):
                raise MissingAPIKeyError(
                    "GOOGLE_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not TRUE."
                )
        #We'll set the capabilities to streaming, which will allow us to stream the response back to the client.
        capabilities = AgentCapabilities(streaming=True)

        skill = AgentSkill(
            id="check_schedule",
            name="Check Karley's Schedule",
            description="Checks Karley's availability for a pickleball game on a given date.",
            tags=["scheduling", "calendar"],
            examples=["Is Karley free to play pickleball tomorrow?"],
        )
        # Define Karley's AgentCard, allowing the host agent to know what Karley's Agent can do.
        agent_card = AgentCard(
            name="Karley Agent",
            description="An agent that manages Karley's schedule for pickleball games.",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            defaultInputModes=["text/plain"],
            defaultOutputModes=["text/plain"],
            capabilities=capabilities,
            skills=[skill],
        )

        adk_agent = create_agent()
        #ADK native feature: to create the agent, we'll need to setup a runner that includes the agent details and memory locations.
        runner = Runner(
            app_name=agent_card.name,
            agent=adk_agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

        #We'll create our agent executor, which will be what will bridge the gap between our agent's invoke / kickoff / etc. that actually triggers the agent (the way we trigger the agent would differ between frameworks), and is a crucial standardization step in A2A.
        agent_executor = KarleyAgentExecutor(runner)

        #We'll create our request handler, which will be what will handle the request from the host agent.
        #Evertyine a request is sent, we're going to pass it to our agent executor.
        request_handler = DefaultRequestHandler(
            agent_executor=agent_executor,
            task_store=InMemoryTaskStore(),
        )
        #Spin up our server along with the agent card and request handler. 
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        uvicorn.run(server.build(), host=host, port=port)
    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        exit(1)


if __name__ == "__main__":
    main()
