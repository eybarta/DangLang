from typing import Dict, Any
from langchain.agents import AgentExecutor
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from .config import PipelineConfig

class CodePipeline:
    def __init__(self, config: Dict[str, Any]):
        self.config = PipelineConfig(**config)
        self.memory = ConversationBufferMemory()
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize agent registry with available agent types"""
        self.agent_registry = {}
        # Agents will be dynamically imported and initialized here
        # This will be populated when we implement the specific agents

    def _create_agent_executor(self, agent_config: Dict[str, Any]) -> AgentExecutor:
        """Create an agent executor for the given agent configuration"""
        if agent_config['type'] not in self.agent_registry:
            raise ValueError(f"Unknown agent type: {agent_config['type']}")
        
        agent_class = self.agent_registry[agent_config['type']]
        llm = ChatOpenAI(model=agent_config['model'])
        
        agent = agent_class(
            llm=llm,
            description=agent_config['description'],
            tools=agent_config['tools']
        )
        
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=agent.get_tools(),
            memory=self.memory,
            verbose=True
        )

    def _execute_step(self, step_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single pipeline step"""
        if step_config.get('iterative', False):
            return self._execute_iterative_step(step_config, context)
        return self._execute_single_step(step_config, context)

    def _execute_iterative_step(self, step_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a step that requires multiple iterations"""
        max_iterations = step_config.get('max_iterations', 3)
        current_iteration = 0
        result = context

        while current_iteration < max_iterations:
            for agent_config in step_config['agents']:
                agent_executor = self._create_agent_executor(agent_config)
                result = agent_executor.run(
                    input={
                        'goal': self.config.goal,
                        'context': self.config.context,
                        'current_state': result
                    }
                )
                
                # Check if we need another iteration
                if not result.get('needs_iteration', False):
                    return result
            
            current_iteration += 1

        return result

    def _execute_single_step(self, step_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a non-iterative step"""
        result = context
        for agent_config in step_config['agents']:
            agent_executor = self._create_agent_executor(agent_config)
            result = agent_executor.run(
                input={
                    'goal': self.config.goal,
                    'context': self.config.context,
                    'current_state': result
                }
            )
        return result

    def run(self) -> Dict[str, Any]:
        """Run the complete pipeline"""
        context = {
            'goal': self.config.goal,
            'context': self.config.context,
            'artifacts': {}
        }

        for step in self.config.pipeline:
            context = self._execute_step(step.dict(), context)

        return context