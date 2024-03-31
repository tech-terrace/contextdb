import time, os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contextdb.settings')
django.setup()
from playwright.sync_api import Playwright, sync_playwright

from core.models import add_docfile


file_name = None
version = None

def run(playwright: Playwright) -> None:
    global file_name, version
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # get version
    page.goto("https://github.com/vuejs/core/releases")
    version_selector = "#repo-content-pjax-container > div > div:nth-child(3) > section:nth-child(1) > div > div.col-md-9 > div > div.Box-body > div.d-flex.flex-md-row.flex-column > div.d-flex.flex-row.flex-1.mb-3.wb-break-word > div.flex-1 > span.f1.text-bold.d-inline.mr-3 > a"
    page.wait_for_selector(version_selector)
    version = page.query_selector(version_selector).inner_text()
    version = version.replace("v", "")

    page.goto("https://vuejs.org/guide/introduction.html")
    
    # Selector for the container holding the links
    container_selector = "#VPSidebarNav"
    # Wait for the container to be loaded
    page.wait_for_selector(container_selector)
    # Get all <a> elements under the specified container
    links = page.query_selector_all(f"{container_selector} a")

    file_name = f"vuejs@{version}_large.txt"

    # clear the file
    open(file_name, "w").close()

    for link in links:

        link.evaluate("element => element.click()")

        time.sleep(0.5)

        # Get the inner text of the <main> block
        main_content = page.query_selector("main").inner_text()

        with open(file_name, "a", encoding="utf-8") as file:
            file.write(main_content + "\n\n")

    page.goto("https://vuejs.org/api/application.html")

    page.wait_for_selector(container_selector)
    # Get all <a> elements under the specified container
    links = page.query_selector_all(f"{container_selector} a")

    for link in links:

        link.evaluate("element => element.click()")

        time.sleep(0.5)

        # Get the inner text of the <main> block
        main_content = page.query_selector("main").inner_text()

        with open(file_name, "a", encoding="utf-8") as file:
            file.write(main_content + "\n\n")



    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)


file_bytes = open(file_name, "rb")
add_docfile("Vue.js", version, "L", file_name, file_bytes)
