import getTime


def get_articles(soup):
    Articles = []
    paperblock = soup.find('tbody', id='gsc_a_b').find_all(
        'tr', class_='gsc_a_tr')

    for papers in paperblock:
        article = {}
        article['publication_date'] = papers.find('td', class_='gsc_a_y').find(
            'span', class_='gsc_a_h gsc_a_hc gs_ibl').text
        # if publication_date is not found then skip
        if article['publication_date'] == '':
            continue

        firstblock = papers.find('td', class_='gsc_a_t')

        title_link = firstblock.find('a', class_='gsc_a_at')
        article['title'] = title_link.text
        article['link'] = 'https://scholar.google.com/' + title_link['href']

        authors_source = firstblock.find_all('div', class_='gs_gray')
        article['authors'] = authors_source[0].text
        article['source'] = authors_source[1].text

        cited_by_record = []
        cited_by = {}
        try:
            cited_by['cited_by'] = papers.find('td', class_='gsc_a_c').find(
                'a', class_='gsc_a_ac gs_ibl').text
        except:
            cited_by['cited_by'] = '0'
        cited_by['updateTime'] = getTime.currentTime()
        cited_by_record.append(cited_by)
        article['cited_by_record'] = cited_by_record

        Articles.append(article)
    return Articles
