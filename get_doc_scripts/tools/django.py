import requests
import os
import datetime as dt
from get_doc_scripts.document_scraper import GitHubDocumentationScraper
from packaging import version

class DjangoDocumentationScraper(GitHubDocumentationScraper):
    def fetch_version(self):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/tags"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tags = response.json()
        # sort tags by version, ignoring unparseable tags
        valid_tags = []
        for tag in tags:
            try:
                parsed_version = version.parse(tag['name'])
                valid_tags.append((parsed_version, tag))
            except ValueError:
                continue  # Ignore tags that cannot be parsed
        valid_tags.sort(reverse=True)  # Sort by parsed version
        if valid_tags:
            self.version = valid_tags[0][1]['name']
        # get commit date
        url = valid_tags[0][1]['commit']['url']
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        commit = response.json()
        self.release_date = dt.datetime.strptime(commit['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ").date()


scraper = DjangoDocumentationScraper("Django", "django", owner="django", repo="django", extensions=["txt"])

if __name__ == "__main__":
    scraper.run()


