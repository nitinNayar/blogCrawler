import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import argparse
import re

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
        
def get_blog_urls(base_url="https://semgrep.dev/blog/", url_pattern=None):
    """
    Crawl blog page and extract all blog post URLs
    
    Args:
        base_url (str): Base URL of the blog
        url_pattern (str): Optional regex pattern to identify blog posts
        
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
                # Clean up the URL
                if not href.startswith('http'):
                    base_domain = urlparse(base_url).netloc
                    href = f"https://{base_domain}{href}" if not href.startswith('/') else f"https://{base_domain}{href}"
                
                # Check if it's a blog post URL
                if url_pattern:
                    # Use custom pattern if provided
                    if re.search(url_pattern, href):
                        blog_urls.append(href)
                else:
                    # Default behavior: match URLs containing /blog/ that aren't the base blog URL
                    if '/blog/' in href and href != base_url:
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
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Scrape blog posts and convert them to markdown files.')
    parser.add_argument('--base-url', 
                      default='https://semgrep.dev/blog/',
                      help='Base URL of the blog to scrape (default: https://semgrep.dev/blog/)')
    parser.add_argument('--output-dir', 
                      default='blog_posts',
                      help='Directory to save markdown files (default: blog_posts)')
    parser.add_argument('--url-pattern',
                      help='Optional regex pattern to identify blog post URLs (e.g. "/blog/\\d{4}/")')
    
    args = parser.parse_args()
    
    # Get blog URLs by crawling the blog page
    blog_urls = get_blog_urls(base_url=args.base_url, url_pattern=args.url_pattern)
    if blog_urls:
        print(f"Found {len(blog_urls)} blog posts")
        for url in blog_urls:
            print(f"Processing {url}")
            content = extract_blog_content(url)
            save_blog_to_file(url, content, output_dir=args.output_dir)
    else:
        print("No blog URLs found")
