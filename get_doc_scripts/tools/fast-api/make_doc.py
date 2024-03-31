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

    page.goto("https://fastapi.tiangolo.com/reference/openapi/")
    version_selector = ".md-source__fact--version"
    page.wait_for_selector(version_selector)
    version = page.query_selector(version_selector).inner_text()

    
    # Selector for the container holding the links
    container_selector = "body > div.md-container > main > div > div.md-sidebar.md-sidebar--primary > div > div > nav > ul > li.md-nav__item.md-nav__item--active.md-nav__item--section.md-nav__item--nested > nav"
    # Wait for the container to be loaded
    page.wait_for_selector(container_selector)
    # Get all <a> elements under the specified container
    links = page.query_selector_all(f"{container_selector} a")

    file_name = f"fast-api@{version}_large.txt"

    # clear the file
    open(file_name, "w").close()

    # make a list of links
    links = [link.evaluate("element => element.href") for link in links]

    for link in links:

        page.goto(link)
        page.wait_for_selector("article")

        time.sleep(1)

        # Get the inner text of the <main> block
        main_content = page.query_selector("article").inner_text()

        with open(file_name, "a", encoding="utf-8") as file:
            file.write(main_content + "\n\n")



    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)


file_bytes = open(file_name, "rb")
add_docfile("FastAPI", version, "L", file_name, file_bytes)
