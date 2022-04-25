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


class CGUScholar_getlabeluserID(threading.Thread):
    def __init__(self, CGUlabelqueue):
        threading.Thread.__init__(self)
        self.queue = CGUlabelqueue

    def run(self):
        while self.queue.qsize() > 0:
            label_domain = self.queue.get()
            CGUScholar_LabelDomain.LabelCrawl(label_domain)

            sleepTime = random.uniform(0.5, 0.8)
            time.sleep(sleepTime)


def CGUlabelCrawlWorker(labelqueue):
    work_queue = labelqueue
    # 建立兩個 Worker
    CGUlabelWorker1 = CGUScholar_getlabeluserID(work_queue)
    CGUlabelWorker2 = CGUScholar_getlabeluserID(work_queue)
    CGUlabelWorker3 = CGUScholar_getlabeluserID(work_queue)
    CGUlabelWorker4 = CGUScholar_getlabeluserID(work_queue)

    # 讓 Worker 開始處理資料
    CGUlabelWorker1.start()
    CGUlabelWorker2.start()
    CGUlabelWorker3.start()
    CGUlabelWorker4.start()

    # 等待所有 Worker 結束
    CGUlabelWorker1.join()
    CGUlabelWorker2.join()
    CGUlabelWorker3.join()
    CGUlabelWorker4.join()

    print("Done.")
