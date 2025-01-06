from danglang.tools import WebSearchTool

def test_search():
    search_tool = WebSearchTool()
    
    # Test the search tool
    query = "Python design patterns for microservices"
    results = search_tool._run(query)
    
    print(f"Search Results for: {query}\n")
    print(results)

if __name__ == "__main__":
    test_search()