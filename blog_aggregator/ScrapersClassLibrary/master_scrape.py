from ScrapersClassLibrary.all_scrapers import AswathScraper, EugeneScraper, StratecheryScraper, CollaborativeScraper,\
    OSAMScraper, AmnesiaScraper, GatesScraper

if __name__ == '__main__':
    scrapers = (GatesScraper(),)
    for scraper in scrapers:
        print(f'About to try to scrape: {scraper.NAME}')
        # try:
        scraper.get_historical_posts()
        # except:
        #     print(f'Failed somewhere for {scraper.NAME}')

        # scraper.make_html(name=scraper.NAME, folder_name='aswath_posts', template_name='aswath')
        # scraper.make_html(name=scraper.NAME, folder_name='eugene_posts', template_name='eugene')
        # scraper.make_html(name=scraper.NAME, folder_name='Stratechery', template_name='stratechery')
        # scraper.make_html(name=scraper.NAME, folder_name='collaborative_posts', template_name='collab')
        # scraper.make_html(name=scraper.NAME, folder_name='osam_posts', template_name='osam')
        # scraper.make_html(name=scraper.NAME, folder_name='amnesia_posts', template_name='amnesia')
        scraper.make_html(name=scraper.NAME, folder_name='gates_posts', template_name='gates')