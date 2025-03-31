import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def extract_blog_content(url):
    """
    Extract blog content from a given URL and return the text
    
    Args:
        url (str): URL of the blog post
        
    Returns:
        str: Extracted blog content
    """
    try:
        # Send GET request to URL
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text content
        text = soup.get_text()
        
        # Clean up text - remove blank lines and extra spacing
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
        
    except Exception as e:
        print(f"Error extracting content from {url}: {str(e)}")
        return None

def save_blog_to_file(url, content, output_dir="blog_posts"):
    """
    Save blog content to markdown file
    
    Args:
        url (str): URL of the blog post
        content (str): Blog content to save
        output_dir (str): Directory to save files to
    """
    if not content:
        return
        
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename from URL by extracting the blog post slug
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    # Find the blog post slug (typically after 'blog' in the path)
    try:
        blog_index = path_parts.index('blog')
        blog_name = '-'.join(path_parts[blog_index + 1:])  # Join all parts after 'blog'
    except ValueError:
        # Fallback if 'blog' is not in the path
        blog_name = path_parts[-1] if path_parts[-1] else 'untitled'
    
    filename = os.path.join(output_dir, f"{blog_name}.md")
    
    # Save content to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Source: {url}\n\n")
        f.write(content)
        
def process_blog_urls(urls):
    """
    Process list of blog URLs and save content
    
    Args:
        urls (list): List of blog URLs to process
    """
    for url in urls:
        print(f"Processing {url}")
        content = extract_blog_content(url)
        save_blog_to_file(url, content)
        
def get_blog_urls(base_url="https://semgrep.dev/blog/"):
    """
    Crawl Semgrep's blog page and extract all blog post URLs
    
    Args:
        base_url (str): Base URL of the blog
        
    Returns:
        list: List of blog post URLs
    """
    try:
        # Setup Chrome in headless mode
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode (no GUI)
        driver = webdriver.Chrome(options=options)
        
        print(f"Fetching page: {base_url}")
        driver.get(base_url)
        
        # Wait for the content to load and scroll to load all articles
        print("Waiting for page to load and scrolling...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load
            time.sleep(2)
            
            # Calculate new scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            print(f"Scrolled to height: {new_height}")
            
            # Break if no more new content
            if new_height == last_height:
                break
            last_height = new_height
        
        # Now get the page source after everything is loaded
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        blog_urls = []
        
        # Find all links on the page
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                print(f"\nProcessing link: {href}")
                
                # Clean up the URL
                if not href.startswith('http'):
                    href = f"https://semgrep.dev{href}" if not href.startswith('/') else f"https://semgrep.dev{href}"
                
                print(f"Cleaned URL: {href}")
                
                # Check if it's a blog post URL using multiple criteria
                is_blog_post = False
                if '/blog/' in href:
                    # Check different blog URL patterns
                    if any(str(year) in href for year in range(2020, 2025)):
                        is_blog_post = True
                        print(f"Matched year pattern: {href}")
                    elif href.count('/') >= 4:
                        is_blog_post = True
                        print(f"Matched path depth pattern: {href}")
                    elif any(month in href.lower() for month in ['january', 'february', 'march', 'april', 'may', 'june', 
                                                               'july', 'august', 'september', 'october', 'november', 'december']):
                        is_blog_post = True
                        print(f"Matched month pattern: {href}")
                
                if is_blog_post:
                    print(f"Adding blog URL: {href}")
                    blog_urls.append(href)
        
        # Close the browser
        driver.quit()
        
        final_urls = list(set(blog_urls))  # Remove duplicates
        print(f"\nFinal blog URLs found ({len(final_urls)}):")
        for url in final_urls:
            print(f"- {url}")
            
        return final_urls
        
    except Exception as e:
        print(f"Error crawling blog URLs: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        return []

if __name__ == "__main__":
    # Get blog URLs by crawling the blog page
    blog_urls = get_blog_urls()
    if blog_urls:
        print(f"Found {len(blog_urls)} blog posts")
        process_blog_urls(blog_urls)
    else:
        print("No blog URLs found")
