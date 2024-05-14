import ebooklib
import os
from ebooklib import epub
from bs4 import BeautifulSoup
import requests
from get_doc_scripts.document_scraper import BaseDocumentationScraper


class RubyDocumentationScraper(BaseDocumentationScraper):
    def _run_extraction(self):
        epub_name = f"ruby_on_rails_guides_v{self.version}.epub"
        response = requests.get(f"https://guides.rubyonrails.org/epub/{epub_name}")
        with open(epub_name, "wb") as f:
            f.write(response.content)

        book = epub.read_epub(epub_name)
        text = []
        for item in book.get_items():
           if item.get_type() == ebooklib.ITEM_DOCUMENT:
               soup = BeautifulSoup(item.content, 'html.parser')
               text.append(soup.get_text())
        text = '\n'.join(text)
        
        os.remove(epub_name)
        with open(self.file_name, "w") as f:
            f.write(text)
        



scraper = RubyDocumentationScraper("Ruby on Rails",
                         "ruby", 
                         owner="rails", 
                         repo="rails")
   

if __name__ == "__main__":
    scraper.run()
