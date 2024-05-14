import requests
import re
import datetime as dt
from get_doc_scripts.document_scraper import DocumentationScraper


class ExpressJSDocumentationScraper(DocumentationScraper):
    def fetch_version(self):
        res = requests.get('https://www.npmjs.com/package/express')
        text = res.text
        self.version = re.search(r'\d+\.\d+\.\d+', text).group(0)
        date = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z', text).group(0)
        self.release_date = dt.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').date()
    
    def _href_list(self, links):
        lst = super()._href_list(links)
        # remove all /en/\dx/api links with regex
        filtered_lst = [link for link in lst if not re.search(r'/en/\d+x/api', link)]
        filtered_lst.insert(0, self.base_url)
        return filtered_lst
    
    def _skip_iteration(self, link):
        if link == 'https://expressjs.com/':
            return True
        if '/resources/' in link or '/2x/' in link:
            return True
        return False
    

scraper = ExpressJSDocumentationScraper("Express.js",
                         "https://expressjs.com/en/api.html", 
                         "#navbar", 
                         "expressjs",
                         content_selector="body > section")
   

if __name__ == "__main__":
    scraper.run()