import aiohttp
from bs4 import BeautifulSoup
from app.api.models import SearchResult
from app.utils.cache import cache
from typing import List, Dict
import re
import trafilatura
from urllib.parse import urlparse

class ContentService:
    @cache(ttl=3600)  # Cache content for 1 hour
    async def extract_content(self, results: List[SearchResult], max_chars: int = 10000) -> str:
        """
        Extract content from the top search results to provide context for AI models.
        """
        all_content = []
        total_chars = 0
        
        # If we have no results or can't extract content, provide a fallback
        if not results:
            return "No search results were found for this query."
        
        # First, add the snippets from the search results
        for result in results:
            all_content.append(f"Source: {result.url}\nTitle: {result.title}\nSummary: {result.snippet}\n")
            total_chars += len(result.snippet)
        
        # Try to extract more content from the web pages
        async with aiohttp.ClientSession() as session:
            for result in results:
                if total_chars >= max_chars:
                    break
                    
                try:
                    # Skip certain domains that are likely to block scraping
                    domain = urlparse(result.url).netloc
                    if any(blocked in domain for blocked in ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com']):
                        continue
                        
                    content = await self._fetch_and_extract(session, result.url)
                    # Limit content per page to ensure we get a mix of sources
                    content = content[:2000]
                    
                    if content:
                        all_content.append(f"Additional content from {result.url}:\n{content}\n")
                        total_chars += len(content)
                except Exception as e:
                    # Skip this result if there's an error
                    print(f"Error extracting content from {result.url}: {str(e)}")
                    continue
        
        return "\n\n".join(all_content)
    
    async def _fetch_and_extract(self, session: aiohttp.ClientSession, url: str) -> str:
        """
        Fetch a web page and extract its main content.
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status != 200:
                    return ""
                
                html = await response.text()
                
                # Try using trafilatura first (better at extracting main content)
                extracted = trafilatura.extract(html, include_comments=False, include_tables=True)
                if extracted:
                    return extracted
                    
                # Fall back to BeautifulSoup if trafilatura fails
                return self._extract_main_content(html)
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return ""
    
    def _extract_main_content(self, html: str) -> str:
        """
        Extract the main content from an HTML page, removing navigation, ads, etc.
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script, style, and other non-content elements
        for element in soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 'iframe', 'noscript']):
            element.decompose()
            
        # Remove common ad and navigation class names
        for element in soup.find_all(class_=re.compile('(ad|banner|menu|sidebar|footer|header|nav|comment)')):
            element.decompose()
        
        # Try to find the main content
        main_content = None
        for tag in ['main', 'article', 'div[role="main"]', '.main-content', '#content', '#main']:
            main_content = soup.select_one(tag)
            if main_content:
                break
                
        if main_content:
            text = main_content.get_text(separator=' ', strip=True)
        else:
            # If no main content found, use the body
            text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text 