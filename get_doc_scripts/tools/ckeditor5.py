from get_doc_scripts.document_scraper import GitHubDocumentationScraper


class CKEditor5DocumentationScraper(GitHubDocumentationScraper):
    pass


scraper = CKEditor5DocumentationScraper("CKEditor 5", "ckeditor5", owner="ckeditor", repo="ckeditor5", docs_folder="docs")

if __name__ == "__main__":
    scraper.run()