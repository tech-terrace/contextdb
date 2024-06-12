from get_doc_scripts.document_scraper import DocumentationScraper


class AngularDocumentationScraper(DocumentationScraper):
    def _break_iteration(self, link):
        return "angularfire" in link


scraper = AngularDocumentationScraper("Angular", "https://angular.dev/overview", 
                         "#secondaryNav", 
                         "angular", 
                         content_selector='docs-docs',
                         owner="angular", 
                         repo="angular")
   

if __name__ == "__main__":
    scraper.run()

