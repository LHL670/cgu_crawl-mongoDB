import time
import manageMongodb
import CGUScholar_LabelCrawl

# Crawl empty label domain
if __name__ == '__main__':
    print('start')

    # update oldest label then crwal user profile
    while(1):
        labelqueue = manageMongodb.get_labelforupdateCGUScholaruserID()
        CGUScholar_LabelCrawl.CGUlabelCrawlWorker(labelqueue)
        time.sleep(3)
