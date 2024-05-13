from get_doc_scripts.document_scraper import DocumentationScraper


class VueJSDocumentationScraper(DocumentationScraper):
    pass

scraper = VueJSDocumentationScraper("FastAPI",
                         "https://fastapi.tiangolo.com/reference/openapi/", 
                         "body > div.md-container > main > div > div.md-sidebar.md-sidebar--primary > div > div > nav > ul > li.md-nav__item.md-nav__item--active.md-nav__item--section.md-nav__item--nested > nav", 
                         "fast-api", 
                         owner="tiangolo",
                         repo="fastapi")
   

if __name__ == "__main__":
    scraper.run()

