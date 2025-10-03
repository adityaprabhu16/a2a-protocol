from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    InternalError,
    InvalidParamsError,
    Part,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils.errors import ServerError
from agent import SchedulingAgent


class SchedulingAgentExecutor(AgentExecutor):
    """AgentExecutor for the scheduling agent."""
    #Initialize our scheduling agent we defined in agent.py using CrewAI.
    def __init__(self):
        """Initializes the SchedulingAgentExecutor."""
        self.agent = SchedulingAgent()

    # Like usual, we'll implement the execute function which will take in the request context and event queue, and be the entry point for the agent to answer a scheduling question.
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Executes the scheduling agent."""
        if not context.task_id or not context.context_id:
            raise ValueError("RequestContext must have task_id and context_id")
        if not context.message:
            raise ValueError("RequestContext must have a message")

        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        if not context.current_task:
            await updater.submit()
        await updater.start_work()

        if self._validate_request(context):
            raise ServerError(error=InvalidParamsError())

        query = context.get_user_input()
        try:
            #We'll invoke the agent to answer the scheduling question.
            result = self.agent.invoke(query)
            print(f"Final Result ===> {result}")
        except Exception as e:
            print(f"Error invoking agent: {e}")
            raise ServerError(error=InternalError()) from e

        parts = [Part(root=TextPart(text=result))]
        #Once we have the response, we'll add the artifact to the task updater. 
        await updater.add_artifact(parts)
        #Mark the task as complete. This signals to the host agent that the task is done, and it can now begin to access the result (parts) and artifacts.
        await updater.complete()

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handles task cancellation."""
        raise ServerError(error=UnsupportedOperationError())

    def _validate_request(self, context: RequestContext) -> bool:
        """Validates the request context."""
        return False
