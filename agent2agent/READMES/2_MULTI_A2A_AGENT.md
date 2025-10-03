Real world Multi-Agent A2A Workflow:
 - We'll connect to an ADK Agent, Crew AI Agent, and LangGraph Agent.
 - Goal: Use agents to schedule Pickleball based on our friend's availability and when courts are available.
 - We'll use agents to determine friend's availability, as well as pickleball availability tool calls.
 - In the next few years, everyone may have their own personal agent that will work with other personal agents to send messages, plan events, etc.
  - This is a REALLY practical example for that reason.

Breakdown:
 - Host Agent:
   - The personal agent that works on our behalf to communicate with other agents.
   - Has access to a couple tools: list of court availabilities, and booking a court.
   - Because we're trying to use A2A to communicate with other agents, we'll use the A2A agent to communicate with 3 other agents (three other friends).
   - Each of the other agents are all using a different framework than our own. That's the benefit of A2A. We can still communicate with these agents!

- Each of the other friend's agents:
 - All hosted on different servers, with access to a tool that will get the availability.

Next Steps:
 - Review Host Agent (client) worfklow -> Code
 - Review ADK Agent (server) workflow -> Code
 - Review CrewAI Agent (server) workflow -> Code
 - Review LangGraph Agent (server) workflow -> Code
 - Run workflow.

1. Review Host Agent Workflow:
- Some Python OOP to understand: 
  - Generic Python Host Agent, which has a class that will be our ADK Host Agent (sort of like we're extending the Host Agent for our use case and creating ADK Host Agent).
- Run ADK Agent in ADK Web connected to Remote Agents using A2A
- Host Agents will be setup differently than server agents.
- Host Agent can be broken down into Prompt and Tools
 - Prompt: Core instructions, available agents
 - Tools: List of court availabilities, book court, send message
 - send message tool will take in our friend's message, followed by our raw message.
 -Steps:
    1. Create a Host Agent and pass in remote url for each friend.
    2. Prep Agent Creation
      - For each URL (remote server), get AgentCard and save agent information (name, description) to self.agents
    3. Create ADK AGents:
        - Pass in self.agents to root instructions
    4. Send Message:
        - Pass in agent name
        - Make sure we are connected to that agent
        - Send message using A2A protocol to remote agent

Quick ADK Overview:
 - In order to run an ADK Agent via ADK Web, we'll need to create a root agent, which lives inside a file and we would have imported the tools.


Quick Recap:
 - We'll create a Python Host Agent responsible for handling all of the connections.
 - We'll then create an ADK agent.
 - Once we have our ADK agent, we'll return the result via ADK web. 
 - We have our host agent, and we'll be able to check what friends we are connected to.
 