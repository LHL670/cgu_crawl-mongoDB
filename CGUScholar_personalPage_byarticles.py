from cProfile import label
import time
import threading
import CGUScholarCrawl
import checkDataformat
import getIDQueue
import manageMongodb
import random
import webdriver
import CGUScholar_articles
# Worker 類別，負責處理資料


class CGUScholarbyarticles(threading.Thread):
    def __init__(self, CGUqueue):
        threading.Thread.__init__(self)
        self.queue = CGUqueue

    def run(self):
        while self.queue.qsize() > 0:
            user_ID = self.queue.get()
            soup = webdriver.Firefoxwebdriver(user_ID)
            if soup == None:
                    continue
            try:
                personalinfo = CGUScholarCrawl.get_personalpage(soup,user_ID)
                articles = CGUScholar_articles.get_articles(soup)
                if articles == None:
                    continue
                check_personalformat = checkDataformat.personalinfoformat(
                    personalinfo)
            except:
                continue
            # ID和name 為空或格式錯誤時回傳False,格式錯誤修正後回傳rewriteInfo

            if(check_personalformat == True):
                try:
                    fix_personalformat = checkDataformat.errorfixpersonalinfoformat(
                        personalinfo)
                    personalinfo = fix_personalformat
                except:
                    # print('test')
                    continue
            manageMongodb.update_personaldata(personalinfo)
            manageMongodb.add_labeldomain(
                personalinfo['personalData']['label'])
            manageMongodb.update_articles(user_ID,articles)
            sleepTime = random.uniform(0.01, 0.05)
            time.sleep(sleepTime)


def CGUCrawlWorker():
    work_queue = getIDQueue.get_IDqueue_forarticles()
    # 建立兩個 Worker
    CGUWorker1 = CGUScholarbyarticles(work_queue)
    CGUWorker2 = CGUScholarbyarticles(work_queue)
    CGUWorker3 = CGUScholarbyarticles(work_queue)
    CGUWorker4 = CGUScholarbyarticles(work_queue)

    # 讓 Worker 開始處理資料
    CGUWorker1.start()
    CGUWorker2.start()
    CGUWorker3.start()
    CGUWorker4.start()

    # 等待所有 Worker 結束
    CGUWorker1.join()
    CGUWorker2.join()
    CGUWorker3.join()
    CGUWorker4.join()

    print("Done.")


if __name__ == '__main__':
    print('start update by articles')   
    while(1):
        CGUCrawlWorker()
        print("sleep 3 second!")
        time.sleep(3)

    # update null label userID

    # label = manageFirebase.get_emptylabelname()  # limit
    # LabelCrawl("empty", label)
    # CGUCrawlWorker(label)

    # # add label ,userID is null
    # LabelCrawl("empty", None)

    # for testing
    # testdocker()
