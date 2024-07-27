from get_doc_scripts.document_scraper import GitHubDocumentationScraper


class PydanticDocumentationScraper(GitHubDocumentationScraper):
    pass


scraper = PydanticDocumentationScraper("Pydantic", "pydantic", owner="pydantic", repo="pydantic", docs_folder="docs")

if __name__ == "__main__":
    scraper.run()