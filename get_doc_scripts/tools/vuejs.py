from get_doc_scripts.document_scraper import DocumentationScraper


class VueJSDocumentationScraper(DocumentationScraper):
    pass
   
scraper = VueJSDocumentationScraper("Vue.js", 
                                    "https://vuejs.org/guide/introduction.html", 
                                    "#VPSidebarNav", 
                                    "vuejs", 
                                    owner="vuejs", 
                                    repo="core")

if __name__ == "__main__":
    scraper.run()

