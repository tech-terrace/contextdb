from get_doc_scripts.document_scraper import DocumentationScraper

# TODO maybe to use https://github.com/laravel/docs instead

class LaravelDocumentationScraper(DocumentationScraper):
    def _break_iteration(self, link):
        return '/api/' in link
    
    def _skip_link(self, link):
        return 'jetstream.laravel.com' in link

scraper = LaravelDocumentationScraper("Laravel",
                         "https://laravel.com/docs/", 
                         "#indexed-nav", 
                         "laravel", 
                         content_selector="#main-content",
                         owner="laravel",
                         repo="laravel")
   

if __name__ == "__main__":
    scraper.run()

