import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sys
url_list = [ 'url-one' , 'url-two' , 'url-three' , 'url-four' ]



def requete(url):
    match url:
        case 'url-one':
            time.sleep(12)
            return 'i am url one ', url
        case 'url-two':
            time.sleep(4)
            return 'i am url two', url
        case 'url-three':
            time.sleep(6)
            return 'i am url three', url
        case 'url-four':
            time.sleep(8)
            return 'i am url four', url



# -----------   Method one  ----------------------

"""


for url in url_list:
    #print(url)
    ab= requete(url)
    print(ab)


"""




# -----------------  Method two  ------------------

"""

processes = []
with ThreadPoolExecutor(max_workers=10) as executor:


    for url in url_list:
        processes.append(executor.submit(requete, url))


    for task in as_completed(processes):  
        if task.result() is not None:
            print(task.result())
        else:
            print(task.result())

"""



# ------------------------  Method three ----------------------------

"""
"""


processes = []
with ThreadPoolExecutor(max_workers=10) as executor:


    for url in url_list:
        processes.append(executor.submit(requete, url))


    for task in processes:  
        if task.result() is not None:
            print(task.result())
        else:
            print(task.result())
