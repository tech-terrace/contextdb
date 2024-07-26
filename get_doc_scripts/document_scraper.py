import os
import shutil
import stat
import re
import requests
import datetime as dt
import django
from playwright.sync_api import Playwright, sync_playwright
from playwright._impl._errors import TimeoutError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contextdb.settings')
django.setup()

from core.models import add_docfile, version_exists


class BaseDocumentationScraper:
    def __init__(self, name, file_prefix, owner=None, repo=None):
        self.name = name
        self.file_prefix = file_prefix
        self.owner = owner
        self.repo = repo

    def _set_file_name(self):
        self.file_name = f"{self.file_prefix}@{self.version}_large.txt"
    
    def fetch_version(self, page=1):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/releases"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        response = requests.get(url, headers=headers, params={"per_page": 100, "page": page})
        response.raise_for_status()
        releases = response.json()
        version_pattern = re.compile(r'^(?:\w+@|v)?(\d+\.\d+\.\d+(?:\.\d+)?)$')
        
        for release in releases:
            match = version_pattern.match(release['tag_name']) or version_pattern.match(release['name'])
            if match:
                self.version = match.group(1)
                self.release_date = dt.datetime.strptime(release['published_at'], "%Y-%m-%dT%H:%M:%SZ").date()
                self._set_file_name()
                return
        
        # If no version is found and there are more releases, recursively call the next page
        if releases:
            self.fetch_version(page + 1)
        else:
            raise ValueError(f"No valid version found for {self.owner}/{self.repo}")
    
    def _run_extraction(self):
        raise NotImplementedError

    def run(self):
        self.fetch_version()

        exists = version_exists(self.name, self.version)

        if exists:
            print(f"Version {self.version} already exists for {self.name}")
            return

        self._run_extraction()
        
        file_bytes = open(self.file_name, "rb")
        add_docfile(self.name, self.version, "L", self.file_name, file_bytes, self.release_date)

        file_bytes.close()
        # remove the file
        os.remove(self.file_name)


class DocumentationScraper(BaseDocumentationScraper):
    def __init__(self, name, base_url, container_selector, file_prefix, 
                 owner=None, repo=None, content_selector="main", browser="chromium"):
        super().__init__(name, file_prefix, owner, repo)
        self.base_url = base_url
        self.container_selector = container_selector
        self.file_name = None
        self.version = None
        self.release_date = None
        self.content_selector = content_selector
        self.browser = browser

    def setup_browser(self, playwright):
        instance = getattr(playwright, self.browser)
        self.browser = instance.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    
    def _break_iteration(self, link):
        return False
    
    def _skip_iteration(self, link):
        return False
    
    def _href_list(self, links):
        return [link.evaluate("element => element.href") for link in links]

    def navigate_and_extract(self):
        self.page.goto(self.base_url)
        self.page.wait_for_selector(self.container_selector)
        links = self.page.query_selector_all(f"{self.container_selector} a")
        open(self.file_name, "w").close()  # Clear the file
        href_list = self._href_list(links)

        for link in href_list:
            if self._break_iteration(link):
                break
            if self._skip_iteration(link):
                continue
            try:
                self.page.goto(link)
                self.page.wait_for_selector(self.content_selector, timeout=5000)
                main_content = self.page.query_selector(self.content_selector).inner_text()
                with open(self.file_name, "a", encoding="utf-8") as file:
                    file.write(main_content + "\n\n")
            except TimeoutError:
                print(f"Timeout error for {link}")
                continue

    def close_browser(self):
        try:
            self.context.close()
            self.browser.close()
        except Exception as e:
            ...

    def _run_extraction(self):
        with sync_playwright() as playwright:
            self.setup_browser(playwright)
            self.navigate_and_extract()
            self.close_browser()
    

class GitHubDocumentationScraper(BaseDocumentationScraper):
    def __init__(self, name, file_prefix, owner=None, repo=None, extensions=["md", "rst"], docs_folder="docs"):
        super().__init__(name, file_prefix, owner, repo)
        self.extensions = extensions
        self.docs_folder = docs_folder
    
    def _clone_repo(self):
        os.system(f"git clone --depth 1 https://github.com/{self.owner}/{self.repo}.git temp_repo")
    
    def _concatenate_files_recursively(self):
        with open(self.file_name, 'w', encoding='utf-8') as outfile:
            for extension in self.extensions:
                for root, dirs, files in os.walk(f"temp_repo/{self.docs_folder}"):
                    for file in files:
                        if file.endswith(extension):
                            with open(os.path.join(root, file), 'r', encoding='utf-8') as infile:
                                outfile.write(infile.read() + "\n\n")
    
    def _run_extraction(self):
        self._clone_repo()
        self._concatenate_files_recursively()

            # Ensure all files are not read-only
        for root, dirs, files in os.walk('temp_repo', topdown=False):
            for name in files:
                filepath = os.path.join(root, name)
                os.chmod(filepath, stat.S_IWUSR)
            for name in dirs:
                os.chmod(os.path.join(root, name), stat.S_IWUSR)
        
        shutil.rmtree('temp_repo')


