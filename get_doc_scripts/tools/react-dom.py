from get_doc_scripts.document_scraper import DocumentationScraper

class ReactDomDocumentationScraper(DocumentationScraper):
    def __init__(self):
        super().__init__("React-dom", 
                         "https://react.dev/reference/react", 
                         "#__next > div.grid.grid-cols-only-content.lg\\:grid-cols-sidebar-content.\\32 xl\\:grid-cols-sidebar-content-toc > div.lg\\:-mt-16.z-10 > div > div > div > aside > nav > ul", 
                         "react-dom", 
                         owner="facebook", 
                         repo="react")

    def _skip_iteration(self, link):
        return '/react-dom' not in link

if __name__ == "__main__":
    scraper = ReactDomDocumentationScraper()
    scraper.run()