from get_doc_scripts.document_scraper import DocumentationScraper


class SpringBootDocumentationScraper(DocumentationScraper):
    def _skip_iteration(self, link):
        return 'spring-boot/api/java' in link  \
            or 'spring-boot/api/kotlin' in link \
            or 'spring-boot/gradle-plugin/api' in link \
            or 'spring-boot/maven-plugin/api' in link

scraper = SpringBootDocumentationScraper("Spring Boot",
                                         "https://docs.spring.io/spring-boot/index.html",
                                         "body > div.body > div.nav-container > aside > div.panels > div.nav-panel-menu.is-active > nav > ul > li > ul",
                                         "spring-boot", 
                                         content_selector="body > div.body > main > div.content > article",
                                         owner="spring-projects", 
                                         repo="spring-boot")

if __name__ == "__main__":
    scraper.run()

