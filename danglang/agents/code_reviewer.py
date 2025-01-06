from typing import List, Dict, Any, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from .base import BaseAgent
from ..tools import LintRunnerTool

class CodeReviewerAgent(BaseAgent):
    def get_tools(self) -> List[BaseTool]:
        """Get tools for code review"""
        tools = []
        if 'lint_runner' in self.tool_names:
            tools.append(LintRunnerTool())
        return tools

    def plan_agent_actions(
        self,
        intermediate_steps: List[tuple[AgentAction, str]],
        callbacks: CallbackManagerForToolRun = None,
        **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """Plan the next action for the reviewer agent"""
        input_data = kwargs.get('input', {})
        current_state = input_data.get('current_state', {})
        code = current_state.get('code', {}).get('optimized', '')

        if not intermediate_steps:
            # First step: Run linting
            return AgentAction(
                tool='lint_runner',
                tool_input=code,
                log="Running code linting checks"
            )

        # After linting, provide review
        lint_results = intermediate_steps[-1][1]
        return AgentFinish(
            return_values={
                'review_comments': ['Linting feedback based on results'],
                'style_issues': [],
                'needs_changes': bool(lint_results.get('errors') or lint_results.get('warnings'))
            },
            log="Completed code review"
        )