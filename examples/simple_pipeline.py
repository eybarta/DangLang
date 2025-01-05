from danglang.pipeline import CodePipeline

def run_simple_pipeline():
    # Define pipeline configuration
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

    # Handle the results
    if 'code' in result:
        print("Generated Code:")
        print(result['code'].get('optimized', 'No code generated'))
        
        if 'test_results' in result:
            print("\nTest Results:")
            print(f"Tests Run: {result['test_results'].get('tests_run', 0)}")
            print(f"Tests Passed: {result['test_results'].get('tests_passed', 0)}")

        if 'validation_passed' in result:
            print("\nValidation:", 
                  "PASSED" if result['validation_passed'] else "FAILED")

if __name__ == "__main__":
    run_simple_pipeline()