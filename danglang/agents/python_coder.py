from typing import List, Dict, Any
from langchain.tools import BaseTool
from .base import BaseAgent
from ..tools import DocFinderTool, CodeEditorTool

class PythonCoderAgent(BaseAgent):
    """Agent specialized in writing Python code"""

    def get_tools(self) -> List[BaseTool]:
        """Get tools for code writing"""
        tools = []
        if 'doc_finder' in self.tool_names:
            tools.append(DocFinderTool())
        if 'code_editor' in self.tool_names:
            tools.append(CodeEditorTool())
        return tools

    def plan(self, goal: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Plan the code implementation"""
        architecture = context.get('architecture', {})
        design_patterns = context.get('design_patterns', [])

        plan = [
            {
                'step': 'setup_structure',
                'description': 'Set up the code structure based on architecture'
            },
            {
                'step': 'implement_core',
                'description': 'Implement core functionality'
            },
            {
                'step': 'add_documentation',
                'description': 'Add code documentation and type hints'
            },
            {
                'step': 'optimize_code',
                'description': 'Optimize code for performance and readability'
            }
        ]

        return plan

    def execute(self, plan: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the code writing plan"""
        result = {
            'code': {},
            'documentation': '',
            'needs_review': True
        }

        code_editor = next((tool for tool in self.get_tools() 
                          if isinstance(tool, CodeEditorTool)), None)

        for step in plan:
            if step['step'] == 'setup_structure':
                if code_editor:
                    result['code']['structure'] = code_editor._run(
                        code='# TODO: Initial structure',
                        action='create'
                    )
            elif step['step'] == 'implement_core':
                if code_editor:
                    result['code']['core'] = code_editor._run(
                        code='# TODO: Core implementation',
                        action='implement'
                    )
            elif step['step'] == 'add_documentation':
                if code_editor:
                    result['documentation'] = code_editor._run(
                        code=result['code'].get('core', ''),
                        action='document'
                    )
            elif step['step'] == 'optimize_code':
                if code_editor:
                    result['code']['optimized'] = code_editor._run(
                        code=result['code'].get('core', ''),
                        action='optimize'
                    )

        return result