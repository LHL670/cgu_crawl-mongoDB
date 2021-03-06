import get_requests
import getTime
import time
import random


def get_labelIDlist(label):
    print("get_labelIDlist : "+label)
    url = 'https://scholar.google.com.tw/citations?view_op=search_authors&hl=zh-TW&mauthors=label:' + label
    soup = get_requests.urlcontent(url)

    searchPage = True
    tempList = []
    Label = {}
    page = int('0')

    while searchPage == True:
        for i in soup.find_all('div', class_='gsc_1usr'):
            id = i.find('a')['href'].split('user=')[1]
            id.replace(" ", "_")
            # print(id)
            tempList.append(id)

        Label['userID'] = tempList
        try:
            # split nextpage after_author
            try:
                afterAuthor = soup.find('div', id='gsc_authors_bottom_pag').find('button', class_='gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx')[
                    'onclick'].split('after_author\\x3d')[1].split('\\x26astart')[0]
            except:
                afterAuthor = soup.find('div', id='gsc_authors_bottom_pag').find('button', class_='gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx')[
                    'onclick'].split('after_author\\x3d')[1].split('\\x26astart')[0]
            page = str(int(page) + 10)

            # running check

            if (int(page) % 500 == 0):
                print(page + ' ' + label)

            url = 'https://scholar.google.com.tw/citations?view_op=search_authors&hl=zh-TW&mauthors=label:' + \
                label+'&after_author='+afterAuthor+'&astart='+page

            soup = get_requests.urlcontent(url)
        except:
            searchPage == False
            print('crawl the end of the label : ' + label)
            break
        sleeptime = random.uniform(0.05, 0.1)
        time.sleep(sleeptime)
    Label['updateTime'] = getTime.currentTime()
    Label['_id'] = label
    return Label
