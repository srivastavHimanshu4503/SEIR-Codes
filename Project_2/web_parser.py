from bs4 import BeautifulSoup

class WebPageParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")

    def get_title(self):
        # Not all pages define a title
        if self.soup.title and self.soup.title.string:
            return self.soup.title.string.strip()
        return ""

    def get_visible_text(self):
        if not self.soup.body:
            return ""
        return "\n".join(self.soup.body.stripped_strings)
    
    def get_all_hyperlinks(self):
        return [a['href'] for a in self.soup.find_all('a', href=True)]
