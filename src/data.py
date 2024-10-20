import fitz
import os
import src.constants as constants
import spacy
nlp = spacy.load("en_core_web_sm")
def read_file_text(filename: str) -> str:
    '''
    Takes in a filename, opens and parses it, and returns the text
    '''
    if filename[-3:]!="pdf":
        return
    doc = fitz.open(constants.DOCS_DIR+filename)
    all_text = []
    for page_nums in range(0, len(doc), constants.SKIP):
        text_in_group = ""
        for page_num in range(page_nums, page_nums + constants.SKIP):
          if page_num >= len(doc):
            break
          page = doc[page_num]
          page_text = page.get_text().replace('\n', ' ').lower()
          docs = nlp(page_text)
          text = " ".join([token.lemma_ for token in docs])
          text_in_group += text
        all_text.append(text_in_group)
    return all_text

