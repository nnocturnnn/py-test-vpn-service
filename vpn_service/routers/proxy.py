from fastapi import APIRouter
import httpx
from bs4 import BeautifulSoup

router = APIRouter()

async def async_parse_html(content: str):
    soup = BeautifulSoup(content, "html.parser")
    for link in soup.find_all('a', href=True):
        yield link

@router.get("/proxy/{site_name}/{path:path}")
async def proxy(site_name: str, path: str):
    target_url = f"https://{site_name}/{path}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(target_url)

    content = response.text
    parsed_content = []
    async for link in async_parse_html(content):
        original_url = link['href']
        if original_url.startswith('/'):
            link['href'] = f"/proxy/{site_name}{original_url}"
        parsed_content.append(str(link))
    
    return "".join(parsed_content)