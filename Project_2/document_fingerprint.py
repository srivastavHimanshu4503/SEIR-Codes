from web_crawler import WebCrawlerClient
from web_parser import WebPageParser
from collections import defaultdict
import sys
import re

class WebDocumentMatcher:

    def get_url(self):
        if len(sys.argv) < 3:
            raise ValueError("Expected 2 urls: One is missing")
        
        url_1, url_2 = sys.argv[1], sys.argv[2]
        return url_1, url_2

    def get_body_content(self, url_1, url_2):
        doc_1 = WebCrawlerClient(url_1).fetch()
        doc_2 = WebCrawlerClient(url_2).fetch()

        doc_body_1 = WebPageParser(doc_1).get_visible_text()
        doc_body_2 = WebPageParser(doc_2).get_visible_text()

        return doc_body_1, doc_body_2
    
    def get_document_frequency(self, doc_body):
        doc_body = re.findall(r"[A-Za-z0-9]+", doc_body.lower())
        word_frequencies = defaultdict(int)
        for word in doc_body:
            word_frequencies[word] += 1

        return word_frequencies
    
    def generate_hash_code(self, word):
        hash = 0
        p = 53
        m = 1 << 64
        base = 1

        for char in word:
            hash = (hash + ord(char)*base) % m
            base = (base * p) % m

        return hash
    
    def generate_fingerprint(self, doc_frequency):
        simhash_vector = [0]*64

        for word, count in doc_frequency.items():
            hash = self.generate_hash_code(word)
            for i in range(64):
                if (hash >> i) & 1:
                    simhash_vector[i] += count
                else:
                    simhash_vector[i] -= count

        fingerprint = 0
        for idx, bit in enumerate(simhash_vector):
            if bit > 0:
                fingerprint |= (1 << idx)

        return fingerprint
    
    def compare_fingerprints(self, fingerprint_1, fingerprint_2):
        fingerprint_xor = fingerprint_1 ^ fingerprint_2
        count_different_bits = 0
        
        while fingerprint_xor:
            count_different_bits += ( fingerprint_xor & 1 )
            fingerprint_xor >>= 1

        return 64 - count_different_bits
    
    def main(self):
        url_1, url_2 = self.get_url()
        doc_body_1, doc_body_2 = self.get_body_content(url_1, url_2)

        doc_freq_1 = self.get_document_frequency(doc_body_1)
        doc_freq_2 = self.get_document_frequency(doc_body_2)

        fingerprint_1 = self.generate_fingerprint(doc_freq_1)
        fingerprint_2 = self.generate_fingerprint(doc_freq_2)

        commonBits = self.compare_fingerprints(fingerprint_1, fingerprint_2)

        print(f"'{url_1}' fingerprint: {bin(fingerprint_1)}")
        print(f"'{url_2}' fingerprint: {bin(fingerprint_2)}")
        print(f"Commonbits: {commonBits}")

if __name__ == "__main__":
    WebDocumentMatcher().main()

