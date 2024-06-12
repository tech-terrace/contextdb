from get_doc_scripts.document_scraper import GitHubDocumentationScraper


class SvelteDocumentationScraper(GitHubDocumentationScraper):
    pass

scraper = SvelteDocumentationScraper("Svelte", "svelte", owner="sveltejs", repo="svelte", docs_folder="documentation")

if __name__ == "__main__":
    scraper.run()


