from typing import List


from class_library import StratecheryScraper, CollaborativeScraper, AswathScraper, OSAMScraper, SiteScrapper, MoneyBankingScaper,OakTreeScraper

SITES_TO_SCRAPE:List[SiteScrapper] = [StratecheryScraper, CollaborativeScraper, AswathScraper,
                                     OSAMScraper, MoneyBankingScaper, OakTreeScraper]

