from danglang.pipeline import CodePipeline

def test_simple_function():
    # Define a simple task for the pipeline
    pipeline_config = {
        'goal': 'Create a Python function that calculates the fibonacci sequence',
        'context': 'The function should be optimized and include proper error handling',
        'pipeline': [
            {
                'task': 'Plan the architecture',
                'agents': [
                    {
                        'type': 'python_architect',
                        'model': 'gpt-4',  # You can change this to your preferred model
                        'description': 'Design a simple but efficient fibonacci function',
                        'tools': ['web_search']
                    }
                ]
            },
            {
                'task': 'Write the function',
                'iterative': True,
                'max_iterations': 2,
                'agents': [
                    {
                        'type': 'python_coder',
                        'model': 'gpt-4',
                        'description': 'Write an optimized fibonacci function',
                        'tools': ['doc_finder', 'code_editor']
                    },
                    {
                        'type': 'code_reviewer',
                        'model': 'gpt-4',
                        'description': 'Review the fibonacci implementation',
                        'tools': ['lint_runner']
                    },
                    {
                        'type': 'code_double_checker',
                        'model': 'gpt-4',
                        'description': 'Verify the fibonacci implementation',
                        'tools': ['unit_test_runner']
                    }
                ]
            }
        ]
    }

    # Initialize and run the pipeline
    pipeline = CodePipeline(pipeline_config)
    result = pipeline.run()

    # Print the results
    print('\n=== Pipeline Results ===\n')
    
    if 'architecture' in result:
        print('Architecture Design:')
        print(result['architecture'])
        print('\n---\n')
    
    if 'code' in result:
        print('Generated Code:')
        print(result['code'].get('optimized', 'No optimized code generated'))
        print('\n---\n')
    
    if 'review_comments' in result:
        print('Review Comments:')
        for comment in result['review_comments']:
            print(f'- {comment}')
        print('\n---\n')
    
    if 'test_results' in result:
        print('Test Results:')
        print(f"Tests Run: {result['test_results'].get('tests_run', 0)}")
        print(f"Tests Passed: {result['test_results'].get('tests_passed', 0)}")
        print('\n---\n')

if __name__ == "__main__":
    test_simple_function()