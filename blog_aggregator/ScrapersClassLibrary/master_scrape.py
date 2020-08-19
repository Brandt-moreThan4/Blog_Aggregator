from ScrapersClassLibrary.all_scrapers import AswathScraper, EugeneScraper, StratecheryScraper

if __name__ == '__main__':
    scrapers = (AswathScraper(), EugeneScraper(), StratecheryScraper())
    for scraper in scrapers:
        print(scraper.NAME)
