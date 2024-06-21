import os
from get_doc_scripts.document_scraper import GitHubDocumentationScraper

class PlaywrightDocumentationScraper(GitHubDocumentationScraper):
    pass

scraper = PlaywrightDocumentationScraper("Playwright", "playwright", owner="microsoft", repo="playwright", docs_folder="docs")

if __name__ == "__main__":
    scraper.run()