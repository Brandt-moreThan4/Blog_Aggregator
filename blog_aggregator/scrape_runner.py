"""High level module to run my scrapers. """

from class_library import AswathScraper, EugeneScraper, StratecheryScraper, CollaborativeScraper, \
    OSAMScraper, AmnesiaScraper, GatesScraper, SiteScrapper, Posty


def scrape_new_data():
    scrapers = (AswathScraper(), EugeneScraper(), StratecheryScraper(), CollaborativeScraper(),
                OSAMScraper(), AmnesiaScraper(), GatesScraper())

    for scraper in scrapers:
        print(f'About to try to scrape: {scraper.NAME}')
        scraper.get_new_posts()



# scrape = SiteScrapper
#
# new_post = Posty()
# new_post.date = '08/22/2012'
# new_post.title = 'title har'
# new_post.author = 'Aswath Damodaron'
# new_post.body = 'bunch ofnsoup'
# new_post.url = 'url'
# new_post.website = 'webbby'
# new_post.name = 'Aswath Damodaron Blog'
# scrape.add_posts_to_db([new_post])
