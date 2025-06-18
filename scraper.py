import requests
from bs4 import BeautifulSoup
import html2text
import os

from logger import log_success, log_warning, log_error

def get_available_versions():
    # Get all available documentated laravel versions
    try:
        docs_home_url = "https://laravel.com/docs"
        response = requests.get(docs_home_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        version_select = soup.find('select', {'aria-label': 'Laravel version'})

        if not version_select:
            log_error("Error: Could not find the version dropdown menu on the page.")
            return None

        versions = []
        for option in version_select.find_all('option'):
            version_name = option.text.strip()
            url = option.get('value')
            if version_name and url:
                versions.append({'name': version_name, 'url': url})
        
        return versions
    except requests.exceptions.RequestException as e:
        log_error(f"Error fetching the Laravel documentation page: {e}")
        return None

def get_doc_links(base_url):
    # Fetches all documentation page links
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # The navigation container has a 'docs_sidebar' class
        nav_container = soup.find('div', class_='docs_sidebar')

        if not nav_container:
            log_error("Error: Could not find the navigation sidebar (div.docs_sidebar).")
            return None

        links = []
        for a in nav_container.find_all('a', href=True):
            href = a['href']
            if href.startswith('/docs/') or not href.startswith('http'):
                full_url = requests.compat.urljoin(base_url, href)
                links.append(full_url)
        
        # Return a sorted list of unique links
        return sorted(list(set(links)))
    except requests.exceptions.RequestException as e:
        log_error(f"Error fetching the navigation page: {e}")
        return None

def scrape_and_save(url, output_dir):
    # Scrapes a single documentation page, cleans it, and saves it as Markdown.
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. Find the main content area of the page
        content_area = soup.find('section', class_='docs_main')

        if not content_area:
            log_warning(f"Warning: Could not find main content for {url}. Skipping.")
            return

        # 2. Pre-process all code blocks to format them nicely for Markdown
        for code_block in content_area.find_all('div', class_='code-container'):
            lang_tag = code_block.find('code')
            lang = lang_tag.get('data-lang', 'shell') if lang_tag else 'shell'
            copy_target = code_block.find('div', class_='torchlight-copy-target')
            
            if copy_target:
                clean_code = copy_target.get_text(strip=False)
                formatted_code = f"\n```{lang}\n{clean_code}\n```\n"
                code_block.replace_with(soup.new_string(formatted_code))
            else:
                code_block.replace_with(soup.new_string(f"\n```\n{code_block.get_text()}\n```\n"))

        # 3. Convert the cleaned HTML to Markdown
        h = html2text.HTML2Text()
        h.body_width = 0 # Prevent automatic line wrapping
        h.ignore_links = False
        markdown_content = h.handle(str(content_area))

        # 4. Create a filename and save the content
        slug = url.split('/')[-1] or "index"
        filename = f"{slug}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Source: {url}\n\n")
            f.write(markdown_content)
            
        log_success(f"Saved: {filepath}")
        return True

    except requests.exceptions.RequestException as e:
        log_error(f"Error scraping {url}: {e}")
        return False
