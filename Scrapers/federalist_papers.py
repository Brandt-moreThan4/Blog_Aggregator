"""Script for retrieving the text of the federalists papers from 'https://guides.loc.gov/federalist-papers/full-text'
   Script gets the text for each essay and saves it in a word documet in the current directory.
   It is probably not robust at all to any changes in the website at all and I did not include any error checking."""

import os
from docx import Document
import re
import sys
# sys.path.append('C:/Users/15314/source/repos/WebScraping/')
import scrapfunctions as scrappy
file1 = os.path.split(__file__)
file2 = os.path.dirname(__file__)
file3 = os.path.basename(__file__)
file4 = os.path.relpath(__file__)

# @scrappy.time_usage
def main():

    url_home = 'https://guides.loc.gov/federalist-papers/full-text'
    main_soup = scrappy.get_soup(url_home)

    # Get the urls to the pages with the essays from the home page.
    all_urls = get_links(main_soup)
    # Extract the relevant essay text from each of the urls into a big string blob.
    all_text = get_all_essay_text(all_urls)
    
    # Clean up some more spacing in text
    cleaned_text = clean_text(all_text)

    # Convert it to be a word document and save it in the same directory as this file.
    convert_txt_to_word(cleaned_text, destination_path=os.path.dirname(__file__) + '\Federalist Papers.docx')


def get_links(soup):
    """Retrieve the urls to all of the pages that contain the federalist papers content.
        Needs some soup and returns a dictionary"""

    # Links to the documents are in the table of contents page in the only table on the page.
    table_links = soup.tbody.find_all('a') 

    # There are many duplicate urls so add each to a dictionary to prevent going to the same page later on.
    # Can't use a set because then the order is unpredictable right? 
    all_urls = {}
    for link in table_links:
        base_url = extract_base_url(link.get('href'))
        all_urls[base_url] = None

    return all_urls


def extract_base_url(url_string):
    """Extract the root link of the url and only add that so that you don't add the same page multiple times
    There are a bunch of duplicates because many of the links are fragments that point to a specific part of the page."""
    # The url fragment comes after the '#' character
    return url_string.partition('#')[0]


def get_all_essay_text(urls):
    """Get all of the federalist essay text that's on the pages of the provided urls
       takes a dictionary of url strings as the keys and returns"""

    all_essay_text = []
    for link in urls.keys():
        essay_text_on_page = extract_federalist_text(link) 
        all_essay_text.append(essay_text_on_page)

     # Add some extra spacing around new lines to make things look cleaner to read.
    all_essay_text = ''.join(all_essay_text)
    all_essay_text = all_essay_text.replace('\n', '\n\n')

    return all_essay_text



def extract_federalist_text(url_string):
    """Get relevant text from each page. Relevant text being the actual content of the federalist papers.
        Takes a url as a string and outputs the text as a string
    """
    soup = scrappy.get_soup(url_string)
    headers = soup.findAll('h2')

    all_essay_text_on_page = []
    for header in headers:
        if header.getText().strip() != 'Table of Contents': # Don't want the text around the table of contents.
            all_essay_text_on_page.append(header.parent.getText().strip()) # Header parent contains the relevant text we want.
            all_essay_text_on_page.append('\n\n\n\n\n') # Add some spacing between each essay.

    return ''.join(all_essay_text_on_page)


def convert_txt_to_word(text, destination_path='Federalist Papers.docx'):
    """Takes text string and saves it as a word document"""
    doc = Document()
    doc.add_paragraph(text)
    doc.save(destination_path)


def clean_text(text):
    """ Takes a string and returns a cleaner string with less spacing."""
    
    # Match all essay headers with regex and trim the new line spacing a bit.....
    # There has got to be a better way.

    findy = re.findall('Federalist No\. \d+\s*', text)

    # Clean text starts out dirty before scrubbing.
    cleaned_text = text

    for old_string in findy:
        new_string = old_string.replace('\n\n', '\n')
        cleaned_text = cleaned_text.replace(old_string,new_string)

    return cleaned_text


if __name__ == "__main__":    
    try:
        main()
    except:
        print('Welp. Something screwed up somewhere so that is a bummer huh!?')