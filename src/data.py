from PyPDF2 import PdfReader
import os
import src.constants as constants
import spacy
nlp = spacy.load("en_core_web_sm")
def read_file_text(filename):
    '''
    Takes in a filename, opens and parses it, and returns the text as a generator
    '''
    doc = PdfReader(filename)
    num_pages=len(doc.pages) 
    print(num_pages)
    for page in doc.pages:
        page.extract_text
    for page_nums in range(0, num_pages, constants.SKIP): 
        print("Starting at page number :", page_nums)
        text_in_group = ""
        
        for page_num in range(page_nums, page_nums + constants.SKIP):  
            print("Reading page number ", page_num)
            if page_num >= num_pages-1:
                return text_in_group 
            page_text = doc.pages[page_num].extract_text()
            page_text = page_text.replace('\n', ' ').lower()
            docs = nlp(page_text)
            text = " ".join([token.lemma_ for token in docs])
            text_in_group += text
        yield text_in_group
    