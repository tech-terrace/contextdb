from get_doc_scripts.document_scraper import DocumentationScraper

class ReactDocumentationScraper(DocumentationScraper):
    def __init__(self):
        super().__init__("React", "https://react.dev/reference/react", "#__next > div.grid.grid-cols-only-content.lg\\:grid-cols-sidebar-content.\\32 xl\\:grid-cols-sidebar-content-toc > div.lg\\:-mt-16.z-10 > div > div > div > aside > nav > ul", "react", owner="facebook", repo="react")

    def _break_iteration(self, link):
        href = link.get_attribute("href")
        return 'react-dom' in href

if __name__ == "__main__":
    scraper = ReactDocumentationScraper()
    scraper.run()