from typing import List, Dict, Any, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from .base import BaseAgent
from ..tools import DocFinderTool, CodeEditorTool

class PythonCoderAgent(BaseAgent):
    def get_tools(self) -> List[BaseTool]:
        """Get tools for code writing"""
        tools = []
        if 'doc_finder' in self.tool_names:
            tools.append(DocFinderTool())
        if 'code_editor' in self.tool_names:
            tools.append(CodeEditorTool())
        return tools

    def plan_agent_actions(
        self,
        intermediate_steps: List[tuple[AgentAction, str]],
        callbacks: CallbackManagerForToolRun = None,
        **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """Plan the next action for the coder agent"""
        input_data = kwargs.get('input', {})
        goal = input_data.get('goal', '')
        context = input_data.get('context', '')
        current_state = input_data.get('current_state', {})

        if not intermediate_steps:
            # First step: Look up documentation
            return AgentAction(
                tool='doc_finder',
                tool_input=goal,
                log=f"Looking up documentation for {goal}"
            )

        if len(intermediate_steps) == 1:
            # Second step: Write initial code
            docs = intermediate_steps[0][1]
            return AgentAction(
                tool='code_editor',
                tool_input={'code': '# TODO: Initial implementation', 'action': 'create'},
                log="Writing initial code implementation"
            )

        # Final step: Return the code
        return AgentFinish(
            return_values={
                'code': {
                    'optimized': intermediate_steps[-1][1],
                    'documentation': '# Code documentation'
                },
                'needs_review': True
            },
            log="Completed code writing"
        )