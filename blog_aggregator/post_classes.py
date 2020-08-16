"""Contains classes used in the aswath scrapper"""




class Post():
    date = ''
    title = ''
    body = ''


    def convert_date(self):
        """Try to convert the text date to datetime, but if it does not work then keep it
        as a string"""
        # This is sketch. I should not allow the possibility for self.date to be two different types.
        try:
            self.date = datetime.datetime.strptime(self.date, '%A, %B %d, %Y')
        except:
            pass

    def __str__(self):
        return str(f'{self.date}\n{self.title}\n{self.body}')





# IMG_FOLDER = Path(r'C:\Users\15314\source\repos\WebScraping\blog_aggregator\images')
# cd = Path.cwd()

# from pathlib import Path
# import sys
# import urllib
# import datetime

# sys.path.append('C:/Users/15314/source/repos/WebScraping/Scrapers')
# import scrapfunctions as scrappy

# class Image():
#     """Represents an image downloaded from some url"""


#     def __init__(self, img_tag, post):
#         self.post = post        
#         try:
#             self.url = img_tag.parent['href']
#         except:
#             self.url = img_tag['src']

#         self.name = self.url.split('/')[-1]
#         self.post_dir = IMG_FOLDER / scrappy.format_filename(self.post.title.strip())    
#         self.image_path = self.post_dir / self.name
#         self.image_saved = False
#         self.save_image()


#     def save_image(self):
#         """Save a blog image in the folder"""
#         self.make_post_directory()
#         # try:
#         with self.image_path.open('wb') as imagefile:
#             imagefile.write(urllib.request.urlopen(self.url).read())
#             self.image_saved = True
#         # except:
#         #      pass 
    

#     def make_post_directory(self):
#         if not self.post_dir.exists():
#             self.post_dir.mkdir()


