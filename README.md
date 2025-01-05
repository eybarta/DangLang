# DangLang

A LangChain-based pipeline for orchestrating multiple AI agents to plan, write, and review Python code.

## Overview

DangLang is a sophisticated Python code generation pipeline that uses multiple specialized AI agents to:
1. Plan the architecture
2. Write optimized code
3. Review and improve the code
4. Double-check for bugs and consistency

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from danglang.pipeline import CodePipeline

# Define your pipeline configuration
pipeline_config = {
    'goal': 'Output elegant and optimized code',
    'context': 'My Python coding team of experts',
    'pipeline': [
        {
            'task': 'Plans the architecture of the python service',
            'agents': [
                {
                    'type': 'python_architect',
                    'model': 'Llama baba gaga',
                    'description': 'A python architect agent that specializes in python architecture and design patterns',
                    'tools': ['web_search']
                }
            ]
        },
        {
            'task': 'Write optimized python service',
            'iterative': True,
            'max_iterations': 3,
            'agents': [
                {
                    'type': 'python_coder',
                    'model': 'Mixtral 100X',
                    'description': 'A python coder agent that can write optimized python code',
                    'tools': ['doc_finder', 'code_editor']
                },
                {
                    'type': 'code_reviewer',
                    'model': 'GTP o9',
                    'description': 'A code reviewer agent that can review the code and provide feedback',
                    'tools': ['lint_runner']
                },
                {
                    'type': 'code_double_checker',
                    'model': 'GPT o2',
                    'description': 'A code double checker agent that ensures no bugs are introduced',
                    'tools': ['unit_test_runner']
                }
            ]
        }
    ]
}

# Initialize and run the pipeline
pipeline = CodePipeline(pipeline_config)
result = pipeline.run()
```

## Project Structure

```
danglang/
├── __init__.py
├── agents/
│   ├── __init__.py
│   ├── base.py
│   ├── python_architect.py
│   ├── python_coder.py
│   ├── code_reviewer.py
│   └── code_double_checker.py
├── tools/
│   ├── __init__.py
│   ├── web_search.py
│   ├── doc_finder.py
│   ├── code_editor.py
│   ├── lint_runner.py
│   └── unit_test_runner.py
├── pipeline.py
└── config.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License