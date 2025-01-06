from typing import List, Dict, Any
from abc import ABC, abstractmethod
from langchain_core.agents import Agent, AgentAction, AgentFinish
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import BaseMessage

class BaseAgent(Agent, ABC):
    """Base agent class that all specialized agents should inherit from"""
    
    def __init__(self, llm: BaseLanguageModel, description: str, tools: List[str]):
        """Initialize the base agent
        
        Args:
            llm: Language model to use for the agent
            description: Description of the agent's role and capabilities
            tools: List of tool names this agent can use
        """
        self.llm = llm
        self.description = description
        self.tool_names = tools
        super().__init__()

    @abstractmethod
    def get_tools(self) -> List[BaseTool]:
        """Get the list of tools this agent can use
        
        Returns:
            List of LangChain Tool instances
        """
        pass

    @abstractmethod
    def plan(self, goal: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Plan the steps to achieve the given goal
        
        Args:
            goal: The goal to achieve
            context: Current context and state
            
        Returns:
            List of planned steps
        """
        pass

    @abstractmethod
    def execute(self, plan: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the planned steps
        
        Args:
            plan: List of planned steps to execute
            context: Current context and state
            
        Returns:
            Updated context/state after execution
        """
        pass

    def get_allowed_tools(self) -> List[str]:
        """Get the list of tool names this agent is allowed to use"""
        return self.tool_names

    @property
    def input_keys(self) -> List[str]:
        """Get the expected input keys for this agent"""
        return ["input"]

    def plan_agent_actions(
        self,
        intermediate_steps: List[tuple[AgentAction, str]],
        callbacks: CallbackManagerForToolRun = None,
        **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """Plan the next action based on intermediate steps"""
        # This method should be implemented by specific agents if needed
        return AgentFinish(
            return_values={"output": "Task completed"},
            log="Agent has finished its execution",
        )