import os
import aiohttp
import requests
from typing import Optional, Dict, Any, ClassVar
from dotenv import load_dotenv
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun

load_dotenv()

BRAVE_API_KEY = os.getenv('BRAVE_API_KEY')
BRAVE_SEARCH_URL = 'https://api.search.brave.com/res/v1/web/search'

class WebSearchTool(BaseTool):
    """Tool for performing web searches using Brave Search API"""
    
    name: ClassVar[str] = "web_search"
    description: ClassVar[str] = "Search the web for information about programming, best practices, and documentation"

    def _process_results(self, response_data: Dict[str, Any]) -> str:
        """Process the Brave Search API results into a readable format
        
        Args:
            response_data: Raw API response data
            
        Returns:
            Formatted search results as a string
        """
        if not response_data.get('web', {}).get('results'):
            return "No results found."
            
        results = response_data['web']['results']
        formatted_results = []
        
        for result in results[:5]:  # Get top 5 results
            title = result.get('title', 'No title')
            description = result.get('description', 'No description')
            url = result.get('url', 'No URL')
            
            formatted_result = f"\nTitle: {title}\nDescription: {description}\nURL: {url}\n"
            formatted_results.append(formatted_result)
            
        return '\n---\n'.join(formatted_results)

    def _run(
        self, 
        query: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute the web search using Brave Search API
        
        Args:
            query: Search query string
            run_manager: Callback manager for the tool run
            
        Returns:
            Search results as a formatted string
        """
        if not BRAVE_API_KEY:
            raise ValueError("BRAVE_API_KEY not found in environment variables")

        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip',
            'X-Subscription-Token': BRAVE_API_KEY
        }
        
        params = {
            'q': query,
            'count': 5,  # Number of results to return
            'search_lang': 'en',
            'safesearch': 'moderate',
            'text_decorations': False,
            'text_format': 'plain'
        }
        
        try:
            response = requests.get(
                BRAVE_SEARCH_URL,
                headers=headers,
                params=params
            )
            response.raise_for_status()
            results = self._process_results(response.json())
            return results
            
        except requests.exceptions.RequestException as e:
            return f"Error performing web search: {str(e)}"

    async def _arun(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute the web search asynchronously
        
        Args:
            query: Search query string
            run_manager: Callback manager for the tool run
            
        Returns:
            Search results as a formatted string
        """
        if not BRAVE_API_KEY:
            raise ValueError("BRAVE_API_KEY not found in environment variables")

        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip',
            'X-Subscription-Token': BRAVE_API_KEY
        }
        
        params = {
            'q': query,
            'count': 5,
            'search_lang': 'en',
            'safesearch': 'moderate',
            'text_decorations': False,
            'text_format': 'plain'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(BRAVE_SEARCH_URL, headers=headers, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return self._process_results(data)
                    
        except aiohttp.ClientError as e:
            return f"Error performing web search: {str(e)}"