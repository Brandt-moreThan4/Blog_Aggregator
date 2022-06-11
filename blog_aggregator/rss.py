from scrapefunctions import get_soup
# from prefect import tasks


STRATECHERY_RSS_URL = 'https://rss.stratechery.passport.online/feed/rss/M5obc3noa81xuSLPuuEYif'

# strat_soup = get_soup(STRATECHERY_RSS_URL,'xml')

# articles = strat_soup.find_all('item')



# ASWATH_RSS = 'https://aswathdamodaran.blogspot.com/feeds/posts/default'
# aswath_soup = get_soup(ASWATH_RSS,'xml')

# articles = aswath_soup.find_all('id')


COLLAB_RSS = 'http://feeds.feedburner.com/collabfund'
collab_soup = get_soup(COLLAB_RSS)

articles = collab_soup.find_all('item') 
# guid.text # This is the permalink


















print('done')