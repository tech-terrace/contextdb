import os
import time
import requests
import datetime as dt
import django
from playwright.sync_api import Playwright, sync_playwright

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contextdb.settings')
django.setup()

from core.models import add_docfile, version_exists

class DocumentationScraper:
    def __init__(self, name, base_url, container_selector, file_prefix, owner=None, repo=None):
        self.name = name
        self.base_url = base_url
        self.container_selector = container_selector
        self.file_prefix = file_prefix
        self.file_name = None
        self.version = None
        self.owner = owner
        self.repo = repo
        self.release_date = None

    def setup_browser(self, playwright):
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def fetch_version(self):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/releases"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        releases = response.json()
        if releases:
            self.version = releases[0]['tag_name'].replace("v", "")
            self.release_date = dt.datetime.strptime(releases[0]['published_at'], "%Y-%m-%dT%H:%M:%SZ").date()
    
    def _break_iteration(self, link):
        return False
    
    def _skip_iteration(self, link):
        return False

    def navigate_and_extract(self):
        self.page.goto(self.base_url)
        self.page.wait_for_selector(self.container_selector)
        links = self.page.query_selector_all(f"{self.container_selector} a")
        self.file_name = f"{self.file_prefix}@{self.version}_large.txt"
        open(self.file_name, "w").close()  # Clear the file

        for link in links:
            if self._break_iteration(link):
                break
            if self._skip_iteration(link):
                continue
            link.evaluate("element => element.click()")
            time.sleep(0.5)
            main_content = self.page.query_selector("main").inner_text()
            with open(self.file_name, "a", encoding="utf-8") as file:
                file.write(main_content + "\n\n")

    def close_browser(self):
        self.context.close()
        self.browser.close()

    def run(self):
        self.fetch_version()

        exists = version_exists(self.name, self.version)

        if exists:
            print(f"Version {self.version} already exists for {self.name}")
            # return

        with sync_playwright() as playwright:
            self.setup_browser(playwright)
            self.navigate_and_extract()
            self.close_browser()
        
        file_bytes = open(self.file_name, "rb")
        add_docfile(self.name, self.version, "L", self.file_name, file_bytes, self.release_date)

        file_bytes.close()
        # remove the file
        os.remove(self.file_name)
