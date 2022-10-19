def getnewestID(url):    
    newestID = url.split('user=')[1].split('&')[0]
    return newestID