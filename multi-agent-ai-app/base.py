# base.py
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the multi-agent AI app.
    Each agent must implement the 'run' method.
    """

    def __init__(self, name: str, role: str, config: Dict[str, Any] = None):
        self.name = name
        self.role = role
        self.config = config or {}
    
    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """
        Execute the main function of the agent.
        Must be implemented by subclasses.
        """
        pass

    def log(self, message: str):
        """Simple logger for the agent."""
        print(f"[{self.name} - {self.role}]: {message}")

    def update_config(self, new_config: Dict[str, Any]):
        """Update agent configuration."""
        self.config.update(new_config)
        self.log("Configuration updated.")
