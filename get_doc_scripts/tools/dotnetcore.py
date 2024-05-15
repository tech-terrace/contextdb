import time
import requests
import fitz
import os
from get_doc_scripts.document_scraper import DocumentationScraper


class DotnetCoreDocumentationScraper(DocumentationScraper):
    def navigate_and_extract(self):
        self.page.goto(self.base_url)
        self.page.wait_for_selector(self.container_selector)
        url = None
        def handle_request(request):
            nonlocal url
            print(f"Intercepted request: {request.url}")
            if 'pdf?' in request.url:
                print("PDF found")
                url = request.url

        self.page.on("request", handle_request)
        
        self.page.click(self.container_selector)

        while not url:
            time.sleep(1)
        
        self.page.close()
        self.browser.close()
        
        # download big pdf in chunks
        response = requests.get(url, stream=True)
        with open('download.pdf', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        self.convert_pdf_to_text('download.pdf')

        # remove pdf
        os.remove('download.pdf')

    def convert_pdf_to_text(self, pdf_path):
        doc = fitz.open(pdf_path)
        
        with open(self.file_name, 'w', encoding='utf-8') as f:
            for page in doc:
                text = page.get_text()
                f.write(text)
                





scraper = DotnetCoreDocumentationScraper("ASP.NET Core",
                         "https://learn.microsoft.com/en-us/aspnet/core/fundamentals/apis", 
                         "#affixed-left-container > div.padding-xxs.padding-none-tablet.border-top.border-bottom-tablet > button > span:nth-child(2)",
                         "dotnetcore", 
                         content_selector="#main > div.content",
                         owner="dotnet",
                         repo="aspnetcore")
   

if __name__ == "__main__":
    scraper.run()

