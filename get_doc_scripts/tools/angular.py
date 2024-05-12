from get_doc_scripts.document_scraper import DocumentationScraper


class AngularDocumentationScraper(DocumentationScraper):
    def __init__(self):
        super().__init__("Angular", "https://angular.io/docs", 
                         "body > aio-shell > mat-sidenav-container > mat-sidenav > div > aio-nav-menu > nav", 
                         "angular", 
                         owner="angular", 
                         repo="angular")
    
    def _break_iteration(self, link):
        return "contributors guide" in link

   

if __name__ == "__main__":
    scraper = AngularDocumentationScraper()
    scraper.run()

