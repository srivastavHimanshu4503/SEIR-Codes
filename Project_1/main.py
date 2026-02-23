# Importing required modules
import sys
from web_crawler import WebCrawlerClient
from web_parser import WebPageParser


class WebCrawlerProject:
    def run(self):
        try:
            if len(sys.argv) <= 1:
                raise ValueError("ERROR: URL Required")
            
            url = sys.argv[1]
            html = WebCrawlerClient(url).fetch()
            parser = WebPageParser(html)
            
            print(f"Title of webpage: {parser.get_title()}")
            print()


            print("Body Text of webpage:")
            print(parser.get_visible_text())
            print()

            print("Hyperlinks: ")
            for link in parser.get_all_hyperlinks():
                print(link)
            print()

        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    WebCrawlerProject().run()