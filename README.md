# BlogCrawler

A powerful Python utility that efficiently crawls and extracts content from blog websites, saving articles as clean markdown files for reference, analysis, or LLM training data.

## Overview

BlogCRawler is a specialized web scraping tool designed to help you collect and archive blog content from websites. It navigates through blog pages, extracts the content, cleans up the text, and saves each article as a markdown file for easy reference.

Key features:
- Automated blog discovery through intelligent crawling
- Clean content extraction with BeautifulSoup
- Scrolling capability to handle dynamically loaded content
- Duplicate URL detection and removal
- Organized storage of blog posts as markdown files

## Use Cases

- Building a personal knowledge base of technical articles
- Creating a corpus of training data for large language models (LLMs)
- Archiving blog content for offline reading
- Research and analysis of blog content
- Preserving content from websites you own or have permission to scrape

## Installation

### Prerequisites

- Python 3.6+
- Chrome or Chromium browser (for Selenium)

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/nitinNayar/blogCrawler.git
   cd blogharvest
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install ChromeDriver for Selenium:
   - Download the appropriate version for your Chrome browser from [ChromeDriver website](https://sites.google.com/chromium.org/driver/)
   - Add it to your PATH or specify its location in the script

## Usage

You can run the script with various command-line arguments to customize its behavior:

### Basic Usage

```bash
python blogs_to_md.py
```

This will use the default settings:
- Base URL: https://semgrep.dev/blog/
- Output Directory: ./blog_posts/

### Command Line Options

```bash
# Specify a different blog URL to scrape
python blogs_to_md.py --base-url https://example.com/blog/

# Specify a custom output directory
python blogs_to_md.py --output-dir my_blog_posts

# Use a custom regex pattern to identify blog posts
python blogs_to_md.py --url-pattern "/blog/\d{4}/"

# Combine multiple options
python blogs_to_md.py --base-url https://example.com/blog/ --output-dir my_blog_posts --url-pattern "/blog/\d{4}/"
```

Available options:
- `--base-url`: The base URL of the blog to scrape (default: https://semgrep.dev/blog/)
- `--output-dir`: Directory where markdown files will be saved (default: blog_posts)
- `--url-pattern`: Optional regex pattern to identify blog post URLs (e.g. "/blog/\d{4}/" to match URLs containing /blog/ followed by a 4-digit year)

To see all available options:
```bash
python blogs_to_md.py --help
```

## How It Works

1. **Configuration**: The tool accepts command-line arguments to customize:
   - The base URL of the blog to scrape
   - The output directory for markdown files
   - Custom regex patterns to identify blog post URLs

2. **Dynamic Content Loading with Selenium**: 
   Many modern blogs load content dynamically as the user scrolls down the page (infinite scrolling). To handle this:
   
   - The tool uses Selenium WebDriver to launch a headless Chrome browser
   - It navigates to the specified blog index page
   - It executes JavaScript to scroll to the bottom of the page repeatedly
   - After each scroll, it waits for new content to load (2 seconds by default)
   - It continues scrolling until no new content appears (detected by comparing page heights)
   - Once all content is loaded, it extracts the fully rendered HTML
   
   This approach ensures that **all** blog posts are discovered, even those that would only appear after scrolling down multiple times on a real browser.
   
   Benefits:
   - **Complete Data Collection**: Captures all blog posts, not just those visible on initial page load
   - **Works with Modern Websites**: Compatible with JavaScript-heavy sites and single-page applications
   - **Automation**: No manual intervention needed to scroll and discover content
   - **Headless Operation**: Runs in the background without displaying a browser window
   - **Cross-Platform**: Works on any system that supports Chrome and ChromeDriver

3. **URL Discovery and Filtering**:
   - Extracts all links from the fully loaded page
   - Cleans and normalizes URLs to ensure they're properly formatted
   - Applies custom regex patterns (if provided) to identify blog post URLs
   - By default, identifies URLs containing "/blog/" that aren't the main blog index
   - Removes duplicate URLs

4. **Intelligent Content Extraction**: For each discovered URL, the tool:
   - Sends an HTTP request to fetch the page content
   - Parses the HTML using BeautifulSoup
   - **Intelligently identifies the main content area** using multiple methods:
     - Looks for semantic HTML5 elements like `<article>` and `<main>`
     - Searches for common blog content class names (e.g., "post-content", "entry-content")
     - Uses a heuristic approach to find the div with the most paragraph content
     - Ranks potential content areas by text length to select the best candidate
   - Removes unwanted elements like headers, footers, navigation, scripts, and styles
   - Extracts clean, formatted text with proper paragraph spacing
   - Adds the page title as a Markdown heading
   - Provides fallback mechanisms for reliable extraction on any blog platform

5. **Storage**: Each blog post is saved as a markdown file with:
   - The original URL as a reference
   - Cleaned text content
   - Filename derived from the blog post slug

## Features in Detail

### Intelligent Content Extraction

The tool uses a sophisticated multi-method approach to extract only the relevant content from blog posts, while filtering out navigation menus, sidebars, footers, and other non-content elements:

1. **Semantic HTML Detection**: Identifies content based on semantic HTML5 elements that commonly contain the main content (`<article>`, `<main>`)

2. **Class-based Detection**: Searches for elements with class names commonly used for blog content across various platforms

3. **Heuristic Analysis**: Analyzes the page structure to find the div with the highest concentration of paragraphs and meaningful text

4. **Content Ranking**: Uses text length and other metrics to rank potential content containers and select the most likely main content area

5. **Fallback Mechanisms**: Includes multiple fallback strategies to ensure content is always extracted, even from non-standard blog layouts

This intelligent extraction results in clean markdown files containing only the actual blog content, making them ideal for:
- Reading without distractions
- Text analysis
- Training AI models
- Knowledge management
- Content preservation

## Ethical Considerations

Please use this tool responsibly and ethically:

- Always respect website terms of service and robots.txt directives
- Implement rate limiting to avoid overloading servers
- Only scrape content from websites where you have permission or the right to do so
- Consider using official APIs when available

## Limitations

- The tool may not extract complex content formats like interactive elements or embedded media
- Some websites use anti-scraping techniques that may prevent successful extraction
- JavaScript-heavy sites might not render completely in headless mode

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Selenium](https://www.selenium.dev/) for browser automation
- [Requests](https://requests.readthedocs.io/) for HTTP functionality