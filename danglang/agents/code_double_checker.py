from typing import List, Dict, Any, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from .base import BaseAgent
from ..tools import UnitTestRunnerTool

class CodeDoubleCheckerAgent(BaseAgent):
    def get_tools(self) -> List[BaseTool]:
        """Get tools for code validation"""
        tools = []
        if 'unit_test_runner' in self.tool_names:
            tools.append(UnitTestRunnerTool())
        return tools

    def plan_agent_actions(
        self,
        intermediate_steps: List[tuple[AgentAction, str]],
        callbacks: CallbackManagerForToolRun = None,
        **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """Plan the next action for the double checker agent"""
        input_data = kwargs.get('input', {})
        current_state = input_data.get('current_state', {})
        code = current_state.get('code', {}).get('optimized', '')

        if not intermediate_steps:
            # First step: Run unit tests
            return AgentAction(
                tool='unit_test_runner',
                tool_input={'code': code, 'test_type': 'unit'},
                log="Running unit tests"
            )

        if len(intermediate_steps) == 1:
            # Second step: Run coverage tests
            return AgentAction(
                tool='unit_test_runner',
                tool_input={'code': code, 'test_type': 'coverage'},
                log="Checking test coverage"
            )

        # Final step: Return validation results
        test_results = intermediate_steps[0][1]
        coverage_results = intermediate_steps[1][1]
        return AgentFinish(
            return_values={
                'validation_passed': test_results.get('success', False),
                'test_results': test_results,
                'coverage_report': coverage_results,
                'needs_iteration': not test_results.get('success', False)
            },
            log="Completed code validation"
        )