"""High level module to run my scrapers. """

from class_library import AswathScraper, EugeneScraper, StratecheryScraper, CollaborativeScraper, \
    OSAMScraper, AmnesiaScraper, GatesScraper, SiteScrapper, Posty


def scrape_new_data():
    # scrapers = (AswathScraper(), EugeneScraper(), StratecheryScraper(), CollaborativeScraper(),
    #             OSAMScraper(), AmnesiaScraper(), GatesScraper())
    scrapers = [OSAMScraper(), CollaborativeScraper()]

    for scraper in scrapers:
        print(f'About to try to scrape: {scraper.NAME}')
        scraper.get_new_posts()


if __name__ == '__main__':
    scrape_new_data()


