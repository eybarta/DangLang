import sys
from danglang.tools import WebSearchTool

def test_search():
    search_tool = WebSearchTool()
    
    # Get query from command line args or use default
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else "Python design patterns for microservices"
    
    print(f"\nExecuting search for: {query}\n")
    results = search_tool._run(query)
    print("Search Results:")
    print("-" * 80)
    print(results)
    print("-" * 80)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("\nUsage: python test_search.py <search query>")
        print("Example: python test_search.py python async patterns\n")
    test_search()