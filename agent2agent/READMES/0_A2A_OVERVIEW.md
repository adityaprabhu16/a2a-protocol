Core Concepts of A2A:
 - STANDARDIZES the way agents communicate with one another.

Example: without A2A:
 - Suppose we're planning a business trip. We'd need to work with a hotel agent to book a flight as well as a car rental agent so we have a car. How do these agents communicate currently? What can a given agent do? How do the agents execute?
 - Whenever we want to build an agent, we not only have to figure out a solution to these questions, but we'd have to implement the same wrappers over and over again so that these agents can understand the requests / responses that are coming from other agents.

What A2A does:
 - We have to do minimal work because the wrappers are already set up.
 - We specify the agents in the system that are available and on which ports (URLs).

Concept 1 of A2A: The AgentCard
 - Answers the "What can an agent do?" question. It's a virtual "business card" that specifies what an agent can do. (see example under READMEs).

Concept 2 of A2A: Standardized Communication
 - Answers the "how do these agents communicate currently?" question.
 - Standardizes a JSON request that other agents supporting A2A can understand. 
 - The "parts" key in the message includes the query.
 - You can also send in context and state which gets sent back in the response, so you can tie things back together in your own thread after you get a response.
 - For longer running requests, we can obtain a Task object, which comes back with several pieces of information (e.g. artifacts which is the agent's thinking, as well as the status (e.g. submitting, working on it, additional inputs needed, completed, canceled, failed)).

Concept 3 of A2A: Agent Executor (How an Agent is Triggered)
 - Denoted by the green "wrapper" around each of the agents in the new A2A paradigm visual.
 - It essentially calls two different functions: Execute and Cancel.
 - AgentExecutor is the thing that gets triggered: takes on an initial request (e.g. Crew AI) or invoke (LangGraph, ADK). It essentially helps kickoff the agent and determines whether to cancel.

Example of Full Flow: Weather Agent
 - We send our request (Get weather for Miami Florida) to our client agent, which has on hand a list of servers (e.g. weather_agent: localhost:1002).
 - Next, the client agent will send the weather agent the message ("Get weather for Miami Florida"), which goes to the server (red), then goes to the weather agent executor (green) (which has a method called execute, which calls the proper function to run our weather agent).
 - The weather agent will think and then send back another message back to the client agent.
 - The client agent will then receive the information, format it, and spit the result back to the client.
