import logging

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    InternalError,
    Part,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils.errors import ServerError
from app.agent import KaitlynAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# As usual, the most important part of our agent executor is the execute function.

class KaitlynAgentExecutor(AgentExecutor):
    """Kaitlyn's Scheduling AgentExecutor."""

    def __init__(self):
        self.agent = KaitlynAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        # Make sure we have access to our task_id and context_id.
        if not context.task_id or not context.context_id:
            raise ValueError("RequestContext must have task_id and context_id")
        if not context.message:
            raise ValueError("RequestContext must have a message")

        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        if not context.current_task:
            await updater.submit()
        # Start working on the task.
        await updater.start_work()

        query = context.get_user_input()
        try:
            async for item in self.agent.stream(query, context.context_id):
                # Based on the different flags, we'll update the task updater accordingly.
                is_task_complete = item["is_task_complete"]
                require_user_input = item["require_user_input"]
                parts = [Part(root=TextPart(text=item["content"]))]

                if not is_task_complete and not require_user_input:
                    await updater.update_status(
                        TaskState.working,
                        message=updater.new_agent_message(parts),
                    )
                elif require_user_input:
                    await updater.update_status(
                        TaskState.input_required,
                        message=updater.new_agent_message(parts),
                    )
                    break
                else:
                    #Once we have the response, we'll add the artifact to the task updater. 
                    #Remember, the artifact gives us a peek inside of the agent's thought process.
                    await updater.add_artifact(
                        parts,
                        name="scheduling_result",
                    )
                    #Mark the task as complete. This signals to the host agent that the task is done, and it can now begin to access the result (parts) and artifacts.
                    await updater.complete()
                    break

        except Exception as e:
            logger.error(f"An error occurred while streaming the response: {e}")
            raise ServerError(error=InternalError()) from e

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise ServerError(error=UnsupportedOperationError())
