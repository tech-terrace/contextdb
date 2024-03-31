import time, os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contextdb.settings')
django.setup()
from playwright.sync_api import Playwright, sync_playwright

from core.models import add_docfile


file_name = None
file_name_text = None

def run(playwright: Playwright) -> None:
    global file_name, file_name_text
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://react.dev/reference/react")
    
        # Selector for the container holding the links
    container_selector = "#__next > div.grid.grid-cols-only-content.lg\\:grid-cols-sidebar-content.\\32 xl\\:grid-cols-sidebar-content-toc > div.lg\\:-mt-16.z-10 > div > div > div > aside > nav > ul"
    # Wait for the container to be loaded
    page.wait_for_selector(container_selector)
    # Get all <a> elements under the specified container
    links = page.query_selector_all(f"{container_selector} a")

    file_name_selector = "#__next > div.grid.grid-cols-only-content.lg\\:grid-cols-sidebar-content.\\32 xl\\:grid-cols-sidebar-content-toc > div.lg\\:-mt-16.z-10 > div > div > div > aside > nav > ul > h3:nth-child(8)"

    file_name_text = page.query_selector(file_name_selector).inner_text()

    file_name = f"{file_name_text}_large.txt"

    # clear the file
    open(file_name, "w").close()

    for link in links:
        # Get the href attribute of the link
        href = link.get_attribute("href")
        
        if '/react-dom' not in href:
            continue 
        # Click on the link if 'react-dom' is not in the href
        link.click()

        time.sleep(0.7)

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
add_docfile("React-dom", file_name_text.split("@")[1], "L", file_name, file_bytes)


