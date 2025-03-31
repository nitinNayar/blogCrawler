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



## How It Works

1. **URL Discovery**: The tool uses Selenium to load the blog index page and scroll through it to discover all blog post URLs.
2. **Content Extraction**: For each URL found, the tool:
   - Sends an HTTP request to fetch the page content
   - Parses the HTML using BeautifulSoup
   - Removes unwanted elements like scripts and styles
   - Extracts the clean text content
3. **Storage**: Each blog post is saved as a markdown file with:
   - The original URL as a reference
   - Cleaned text content
   - Filename derived from the blog post slug

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

## Extending the Tool

You can extend this tool to add features like:

- Custom content extractors for specific blog platforms
- Metadata extraction (author, date, tags)
- Image downloading
- Conversion to different formats (PDF, HTML, etc.)
- Integration with NLP libraries for content analysis

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Selenium](https://www.selenium.dev/) for browser automation
- [Requests](https://requests.readthedocs.io/) for HTTP functionality