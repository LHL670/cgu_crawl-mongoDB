from cProfile import label
import time
import threading
import CGUScholarCrawl
import checkDataformat
import getIDQueue
import CGUScholar_LabelDomain
import requests
import manageMongodb
import random
import webdriver
import CGUScholar_articles
# Worker 類別，負責處理資料


class CGUScholar(threading.Thread):
    def __init__(self, CGUqueue):
        threading.Thread.__init__(self)
        self.queue = CGUqueue

    def run(self):
        while self.queue.qsize() > 0:
            user_ID = self.queue.get()
            soup = webdriver.Firefoxwebdriver(user_ID)
            personalinfo = CGUScholarCrawl.get_personalpage(soup,user_ID)
            articles = CGUScholar_articles.get_articles(soup)
            try:
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
            sleepTime = random.uniform(0.05, 0.1)
            time.sleep(sleepTime)


def CGUCrawlWorker(label):
    work_queue = getIDQueue.get_IDqueue(label)
    # 建立兩個 Worker
    CGUWorker1 = CGUScholar(work_queue)
    CGUWorker2 = CGUScholar(work_queue)
    CGUWorker3 = CGUScholar(work_queue)
    CGUWorker4 = CGUScholar(work_queue)

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


# def testdocker():
#     while 1:
#         url = 'http://httpbin.org/ip'
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
#         }
#         ip = requests.get(url, headers=headers, proxies={
#                           "http": "http://0.0.0.0:8888"}).text
#         if ip:
#             print(ip)
#             time.sleep(10)
#     return


# 累積到一定得筆數upload firebase
if __name__ == '__main__':
    print('start')

    # update oldest label then crwal user profile
    while(1):
        label = manageMongodb.get_labelforCGUScholar()
        print('GET label : ' + label)
        # CGUScholar_LabelDomain.LabelCrawl(label)
        CGUCrawlWorker(label)
        print("sleep 5 second!")
        time.sleep(5)

    # update null label userID

    # label = manageFirebase.get_emptylabelname()  # limit
    # LabelCrawl("empty", label)
    # CGUCrawlWorker(label)

    # # add label ,userID is null
    # LabelCrawl("empty", None)

    # for testing
    # testdocker()
