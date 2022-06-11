import requests

def get_page_response(url):
    """Get a page response using the given url"""
    try:
        page_response = requests.get(url)
    except:
        print('Error loading url')
        return None
    else:
        return page_response


lol = get_page_response("https://www.osam.com/")

print('done')