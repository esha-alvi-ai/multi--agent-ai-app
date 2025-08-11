from logger.logger import Logger

class AgentManager:
    def __init__(self):
        self.logger = Logger(__name__)
        self.agents = {}

    def register_agent(self, name, agent):
        """Register a new agent."""
        if name in self.agents:
            self.logger.warn(f"Agent '{name}' already exists. Overwriting.")
        self.agents[name] = agent
        self.logger.info(f"Registered agent: {name}")

    def get_agent(self, name):
        """Retrieve an agent by name."""
        agent = self.agents.get(name)
        if not agent:
            self.logger.error(f"Agent '{name}' not found.")
        return agent

    def remove_agent(self, name):
        """Remove an agent from the registry."""
        if name in self.agents:
            del self.agents[name]
            self.logger.info(f"Removed agent: {name}")
        else:
            self.logger.warn(f"Tried to remove non-existent agent: {name}")

    def list_agents(self):
        """List all registered agents."""
        return list(self.agents.keys())
