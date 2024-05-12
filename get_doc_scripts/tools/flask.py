from get_doc_scripts.document_scraper import GitHubDocumentationScraper


class FlaskDocumentationScraper(GitHubDocumentationScraper):
    pass

if __name__ == "__main__":
    scraper = FlaskDocumentationScraper("Flask", "flask", owner="pallets", repo="flask")
    scraper.run()


