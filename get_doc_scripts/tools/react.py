from get_doc_scripts.document_scraper import DocumentationScraper

class ReactDocumentationScraper(DocumentationScraper):

    def _break_iteration(self, link):
        return 'react-dom' in link

scraper = ReactDocumentationScraper("React", "https://react.dev/reference/react", "#__next > div.grid.grid-cols-only-content.lg\\:grid-cols-sidebar-content.\\32 xl\\:grid-cols-sidebar-content-toc > div.lg\\:-mt-16.z-10 > div > div > div > aside > nav > ul", "react", owner="facebook", repo="react")


if __name__ == "__main__":
    scraper.run()
