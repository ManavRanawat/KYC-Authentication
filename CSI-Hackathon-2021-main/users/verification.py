from bs4 import BeautifulSoup

def check_exist(response):
    soup = BeautifulSoup(response, 'html.parser')
    #print(soup)
    tags = soup('h2')
    others = soup('b')
    S = []
    for other in others:
        S.append(other.decode()[3:-4])
    if(len(tags)>1):
        return (True,S)
    else:
        return (False,[])