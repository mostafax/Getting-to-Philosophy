from bs4 import BeautifulSoup
import requests
import time
link = "https://en.wikipedia.org/wiki/Special:Random"
dead_lock = []


def call_next(link):
    # to prevent bocking 
    time.sleep(0.5)
    link_checker = None
    content = None
    response = requests.get(link)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # parsing the html tags
    content = soup.find(id="mw-content-text").find(class_="mw-parser-output").find_all('p',recursive=False)
    for tag in content:
        if tag.find('a'):
            try:
                link_checker = tag.find('a',recursive=False).get('href')
                break
            except:
                print("Not link found")
                return
    # check if link exsist 
    if not link_checker:
        print("No link Found")
        return

    concanedated_next_link = "https://en.wikipedia.org"+link_checker
    target_link = "https://en.wikipedia.org/wiki/Philosophy"
    
    if concanedated_next_link == target_link:
        print(concanedated_next_link)
        print("Philosophy section Found")
        return

    else:
        print(concanedated_next_link)
        # Prevent calling the same visited link twice (deadlock)
        if concanedated_next_link in dead_lock:
            return call_next("https://en.wikipedia.org/wiki/Special:Random")
        else:
            dead_lock.append(concanedated_next_link)

        call_next(concanedated_next_link)

call_next(link)