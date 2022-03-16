import time
import manageMongodb
import CGUScholar_LabelDomain

# Crawl empty label domain
if __name__ == '__main__':
    print('start')

    # update oldest label then crwal user profile
    while(1):
        label = manageMongodb.get_emptylabelname()
        CGUScholar_LabelDomain.LabelCrawl(label)
        time.sleep(5)
