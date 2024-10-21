from PyPDF2 import PdfReader
import os
import src.constants as constants
import spacy
nlp = spacy.load("en_core_web_sm")
def read_file_text(filename):
    '''
    Takes in a filename, opens and parses it, and returns the text
    '''
    
    doc = PdfReader(filename)
    num_pages=len(doc.pages)
    
    all_text = []
    for page in doc.pages:
        page.extract_text
    for page_nums in range(0, num_pages, constants.SKIP):
        text_in_group = ""
        for page_num in range(page_nums, page_nums + constants.SKIP):
          if page_num >= num_pages:
            break
          page_text = doc.pages[page_num].extract_text()
          page_text = page_text.replace('\n', ' ').lower()
          docs = nlp(page_text)
          text = " ".join([token.lemma_ for token in docs])
          text_in_group += text
        all_text.append(text_in_group)
    print("text", all_text)
    return all_text

