from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class AgentConfig(BaseModel):
    type: str
    model: str
    description: str
    tools: List[str]

class PipelineStepConfig(BaseModel):
    task: str
    iterative: Optional[bool] = False
    max_iterations: Optional[int] = 1
    agents: List[AgentConfig]

class PipelineConfig(BaseModel):
    goal: str
    context: str
    pipeline: List[PipelineStepConfig]