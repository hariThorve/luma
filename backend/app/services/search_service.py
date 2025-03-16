import aiohttp
from bs4 import BeautifulSoup
from app.api.models import SearchResult
from app.utils.cache import cache
from typing import List
import urllib.parse
import random
import json
import re

class SearchService:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        ]
        
    @cache(ttl=3600)  # Cache results for 1 hour
    async def search(self, query: str, num_results: int = 5) -> List[SearchResult]:
        """
        Perform a search and return the results.
        """
        # Try multiple search engines
        try:
            # First try Google
            google_results = await self._search_with_google(query, num_results)
            if google_results and len(google_results) > 0:
                return google_results
                
            # Then try Bing
            bing_results = await self._search_with_bing(query, num_results)
            if bing_results and len(bing_results) > 0:
                return bing_results
                
            # Finally, use DuckDuckGo
            ddg_results = await self._search_with_ddg(query, num_results)
            if ddg_results and len(ddg_results) > 0:
                return ddg_results
        except Exception as e:
            print(f"Search error: {str(e)}")
            
        # If all search engines fail, return fallback results
        return self._generate_fallback_results(query, num_results)
    
    async def _search_with_google(self, query: str, num_results: int) -> List[SearchResult]:
        """
        Search using Google
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                }
                
                url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num={num_results+5}"
                
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        return []
                    
                    html = await response.text()
                    
                    # Parse the HTML response
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    # Google search results are in divs with class 'g'
                    for div in soup.select('div.g'):
                        # Find the title and URL
                        title_element = div.select_one('h3')
                        if not title_element:
                            continue
                            
                        title = title_element.get_text(strip=True)
                        
                        # Find the URL
                        url_element = div.select_one('a')
                        if not url_element:
                            continue
                            
                        url = url_element.get('href', '')
                        if url.startswith('/url?q='):
                            url = url.split('/url?q=')[1].split('&')[0]
                        elif not url.startswith('http'):
                            continue
                        
                        # Find the snippet
                        snippet_element = div.select_one('div.VwiC3b')
                        snippet = snippet_element.get_text(strip=True) if snippet_element else ""
                        
                        results.append(SearchResult(
                            title=title,
                            url=url,
                            snippet=snippet
                        ))
                        
                        if len(results) >= num_results:
                            break
                    
                    return results
        except Exception as e:
            print(f"Google search error: {str(e)}")
            return []
    
    async def _search_with_bing(self, query: str, num_results: int) -> List[SearchResult]:
        """
        Search using Bing
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                }
                
                url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}&count={num_results+5}"
                
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        return []
                    
                    html = await response.text()
                    
                    # Parse the HTML response
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    # Bing search results are in li elements with class 'b_algo'
                    for li in soup.select('li.b_algo'):
                        # Find the title and URL
                        title_element = li.select_one('h2 a')
                        if not title_element:
                            continue
                            
                        title = title_element.get_text(strip=True)
                        url = title_element.get('href', '')
                        
                        # Find the snippet
                        snippet_element = li.select_one('p')
                        snippet = snippet_element.get_text(strip=True) if snippet_element else ""
                        
                        results.append(SearchResult(
                            title=title,
                            url=url,
                            snippet=snippet
                        ))
                        
                        if len(results) >= num_results:
                            break
                    
                    return results
        except Exception as e:
            print(f"Bing search error: {str(e)}")
            return []
    
    async def _search_with_ddg(self, query: str, num_results: int) -> List[SearchResult]:
        """
        Search using DuckDuckGo
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                }
                
                url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
                
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        return []
                    
                    html = await response.text()
                    
                    # Parse the HTML response
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    # DuckDuckGo search results are in divs with class 'result'
                    for div in soup.select('.result'):
                        # Find the title and URL
                        title_element = div.select_one('.result__title a')
                        if not title_element:
                            continue
                            
                        title = title_element.get_text(strip=True)
                        
                        # Find the URL
                        url = title_element.get('href', '')
                        if url.startswith('/'):
                            url_parts = urllib.parse.urlparse(url)
                            query_params = urllib.parse.parse_qs(url_parts.query)
                            if 'uddg' in query_params:
                                url = query_params['uddg'][0]
                        
                        # Find the snippet
                        snippet_element = div.select_one('.result__snippet')
                        snippet = snippet_element.get_text(strip=True) if snippet_element else ""
                        
                        results.append(SearchResult(
                            title=title,
                            url=url,
                            snippet=snippet
                        ))
                        
                        if len(results) >= num_results:
                            break
                    
                    return results
        except Exception as e:
            print(f"DuckDuckGo search error: {str(e)}")
            return []
    
    def _generate_fallback_results(self, query: str, num_results: int) -> List[SearchResult]:
        """
        Generate fallback results when all search engines fail.
        """
        # Create a more informative fallback result
        return [
            SearchResult(
                title=f"Search for: {query}",
                url=f"https://www.google.com/search?q={urllib.parse.quote(query)}",
                snippet=f"We couldn't find specific information about '{query}'. This might be because the topic is very new, specialized, or not widely documented online. Try refining your search or checking specialized sources."
            )
        ] 