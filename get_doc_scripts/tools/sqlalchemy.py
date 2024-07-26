from get_doc_scripts.document_scraper import GitHubDocumentationScraper


class SQLAlchemyDocumentationScraper(GitHubDocumentationScraper):
    pass


scraper = SQLAlchemyDocumentationScraper("SQLAlchemy", "sqlalchemy", owner="sqlalchemy", repo="sqlalchemy", docs_folder="doc")

if __name__ == "__main__":
    scraper.run()