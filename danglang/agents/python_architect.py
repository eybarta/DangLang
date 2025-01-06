from typing import List, Dict, Any, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from .base import BaseAgent
from ..tools import WebSearchTool

class PythonArchitectAgent(BaseAgent):
    def get_tools(self) -> List[BaseTool]:
        """Get tools for architecture planning"""
        tools = []
        if 'web_search' in self.tool_names:
            tools.append(WebSearchTool())
        return tools

    def plan_agent_actions(
        self,
        intermediate_steps: List[tuple[AgentAction, str]],
        callbacks: CallbackManagerForToolRun = None,
        **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """Plan the next action for the architect agent"""
        input_data = kwargs.get('input', {})
        goal = input_data.get('goal', '')
        context = input_data.get('context', '')
        current_state = input_data.get('current_state', {})

        if not intermediate_steps:
            # First step: Plan architecture
            return AgentAction(
                tool='web_search',
                tool_input=f"Python design patterns and architecture for {goal}",
                log=f"Searching for best practices and patterns for {goal}"
            )
        
        # After search, finish with architecture plan
        search_result = intermediate_steps[-1][1]
        return AgentFinish(
            return_values={
                'architecture': {
                    'patterns': ['Identified patterns based on search'],
                    'components': ['Component breakdown'],
                    'dependencies': ['Required dependencies']
                },
                'documentation': f"Architecture planning based on: {search_result}"
            },
            log="Completed architecture planning"
        )