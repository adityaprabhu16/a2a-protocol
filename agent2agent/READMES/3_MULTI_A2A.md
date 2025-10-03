Overview:
 - We'll create our agent like we normally do, following the specific patterns under our framework to create our specific tools.
 - Once we have the agent and the tool setup, we'll wrap each agent inside of our AgentExecutor.
 - The AgentExecutor will be what will bridge the gap between our agent's invoke / kickoff / etc. that actually triggers the agent (the way we trigger the agent would differ between frameworks), and is a crucial standardization step in A2A.
 - Once our remote agent is wrapped, will kick off our remote server. 
 - We'll then create our AgentCard which will include all of our agent's skills, description, metadata.
 - Pass in AgentExecutor to our server.
 - Pass our AgentExecutor to our Request Handler
 - Once all of our request handlers are spun out, we can then run our remote agent server, which will be sitting there waiting to receive our request.
 - We'll then have to pass in our AgentExecutor to our server 


Remote Agent ADK Example (Karley's Agent):
 - We pass in our general agent, model, tools
 - Define the methods for each of our tools
 - Now Karley's Agent Executor will call an execute function.
 - The execute function will take in a task_id and context_id.
 - The execute function will contain a TaskUpdater that will take in the event_queue, and those different IDs (as discussed in section 0).