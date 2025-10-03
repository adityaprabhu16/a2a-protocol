We'll create:
 - Client Agent
 - The A2A Starlette Application / Server which we'll spin up, along with a Greeting Agent Executor.

Steps:
 - Client makes a request to the A2A server, allowing us to see what agent cards are available.
 - Client will take a look at the available AgentCards to determine the agent it needs, and that message is sent to the server.
 - Request goes to A2A server, followed by AgentExecutor, which executes the Dummy Greeting Agent, which returns a response back to the client.

Files Rundown:
 - __main__.py:
     - Contains the agent card: a business card on what the agent(s) can do (input, output, skills (tools for a given agent), description, name, url / server where the agent is hosted, AgentCapabilities).
     - AgentCapabalities: determines whether everything from the agent is sent back bit by bit, or all at once. Also determines whether we want to poll the agent to see when it's done, OR do push notifications where the agent sends back a notification once it's done. We'll leave it empty for now. 
     - A2A provides a default request handler to makes it easy: determines we want to spin up an agent, which wraps the AgentExecutor, and provides a server to host the agent. (Similar to how the AgentExecutor wraps the actual agent). 
     - For the request handler, we'll specify our agent executor, as well as a task store (e.g. InMemoryTaskStore as a default.)
     - For the server, we'll specify the http_handler (our request_handler from the previous step).
     - uvicorn is what's used to run the server.

 - agent_executor.py
    - The place where we define our custom agent executor that inherits from the AgentExecutor class.
    - Calls execute on our agent (invoke). Everytime the agent runs, it runs asynchronously and then sends back the response.
    - Once we get the response back, we'll get back a message in A2A format which creates a new Message (aka. A message has a role, parts, messageId, taskId - see 0_AGENT_MESSAGE.png if you need a beter understanding of the architecture).

 - test_client.py
    - Essentially, how we will communicate with the server. All the client does is fetch the AgentCard and then start sending messages.
    - First step: we need to first make a request and resolve what capabilities our server has. 
    - We'll have an async A2ACardResolver

- Flow:
     - in one window, run the server
     - in another terminal window, run the test_client

- Understanding the flow:
 -  INFO:     127.0.0.1:51842 - "GET /.well-known/agent.json HTTP/1.1" 200 OK (LOOKING up the AgentCard)
 - A2AClient initialized (after AgentCard is looked up)
 - We'll then send our message we curated for the AgentCard we looked up, and will receive a response.
 - Rummage through the response JSON, and you'll indeed see under "parts", we see the response from our greeting agent.

"parts": [
    {
    "kind": "text",
    "metadata": null,
    "text": "Hello YouTube! Make sure to like and subscribe!"
    }
],

In summary: 
 - A2A made it very easy for us to standardize communication between clients and servers.
 - Made the entire process super seamless and standardized everything.