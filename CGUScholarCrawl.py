from logging import error
import get_requests
import getTime

# personal detail


# personal detail
def get_userprofile(soup):
    info = {}
    d = soup.find('div', id='gsc_prf_i')

    # name
    try:
        info['name'] = d.find('div', id='gsc_prf_in').text

    except Exception as e:
        print('Skip : name format error ')
        print(e)
   #university 
    try:        
        info['university'] = d.find('a', class_='gsc_prf_ila').text 
        if info['university'] == '首頁': 
            info['university'] = d.find('div', class_='gsc_prf_il').text 
    except: 
        try: 
            info['university'] = d.find('div', class_='gsc_prf_il').text 
            print(info['university'] )
        except: 
            info['university'] = ' ' 
    # picture
    try:
        info['picture'] = soup.find('div', id='gsc_prf_pua').find('img')['src']
    except:
        info['picture'] = 'https://scholar.google.com.tw/citations/images/avatar_scholar_128.png'
    label = []
    for p in soup.find_all('a', class_='gsc_prf_inta gs_ibl'):
        ptemp1 = p.text.replace(" ", "_")
        ptemp = ptemp1.replace("-", "_")
        label.append(ptemp)
    info['label'] = label

    return info


def get_CiteBy(soup):
    citeBy = {}
    citations = {}
    h_index = {}
    i10_index = {}

    def cited(status, value):
        if status / 2 < 1:
            if status % 2 == 0:
                citations['All'] = value
            else:
                citations['Since2016'] = value
            citeBy['citations'] = citations
        if status / 2 < 2:
            if status % 2 == 0:
                h_index['All'] = value
            else:
                h_index['Since2016'] = value
            citeBy['h_index'] = h_index
        if status / 2 < 3:
            if status % 2 == 0:
                i10_index['All'] = value
            else:
                i10_index['Since2016'] = value
            citeBy['i10_index'] = i10_index

    count_d = 0
    for d in soup.find_all('td', class_='gsc_rsb_std'):
        cited(count_d, d.text)
        count_d = count_d + 1

    return citeBy


def profileresult(soup, ID):
    infos = {}
    infos['_id'] = ID
    infos['personalData'] = get_userprofile(soup)
    infos['updateTime'] = getTime.currentTime()
    infos['cited'] = get_CiteBy(soup)
    infos['citedRecord'] = [
        {'updateTime': infos['updateTime'], 'cited': infos['cited']}]

    return infos


def get_personalpage(soup,id):
    # url = 'https://scholar.google.com.tw/citations?hl=zh-TW&user=' + id
    # soup = get_requests.urlcontent(url)
    return profileresult(soup, id)
