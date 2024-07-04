#######################################################################################################################################################
### author: hosein aghahoseini @ matin international group
### created at: Oct 08 2023 18:30 GMT+3
### last modified: Oct 09 2023 12:27 GMT+3
### description: This script takes a list of urls( a file name passed to script as a argument) and reports the status code received from each url
#######################################################################################################################################################

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
from colorama import Fore, Style


COLORS = {
    "1xx": Fore.WHITE,
    "2xx": Fore.GREEN,
    "3xx": Fore.YELLOW,
    "4xx": Fore.RED,
    "5xx": Fore.LIGHTRED_EX,
    "Invalid": Fore.WHITE
}

status_codes = {
    "1xx": [],
    "2xx": [],
    "3xx": [],
    "4xx": [],
    "5xx": [],
    "Invalid": []
}



def requete(url):
    # Adding https:// if no protocol is specified

    #Because when the url is valid in any aspect 
    #But only the protocol is not specified 
    # the url is not resolved to the ip  and For this reason, this url is considered invalid
    if "://" not in url:
        url = "https://" + url  


    try:
        #Those urls that resolve to IP  they remain in try block 

        #We specify the timeout Because some urls dosent exist and  not resolved to IP 
        #For this reason, the request function spends a long time to requesting a url which is never going to be resolved to IP
        #With this method, the script runs faster
        r = requests.get(url, timeout=5)
        return url, r.status_code , 'url-valid'
    except:
        #Those urls that  not resolved to IP  they fall into except block 
        return url, "not resolve to ip" , 'url-invalid'
        pass

#If the length of sys.argv is less than 2 
#It means that the file containing the urls is not specified 

#sys.argv with len of one --> python felan.py
#sys.argv with len of two--> python felan.py urls.txt
if len (sys.argv) != 2 :
        print ("Usage: ./" + sys.argv[0] + " [URL list] ")
        sys.exit (1)

       
#Each line in the file x A url is considered      
url_list = [line.rstrip('\n') for line in open(sys.argv[1])]



processes = []
with ThreadPoolExecutor(max_workers=10) as executor:


    #Collecting all future objects in an array
    #Because with this method 
    #We can iterate on the  all of  future objects
    for url in url_list:
        processes.append(executor.submit(requete, url))


    """ 
    processes array be like

    [
        <Future at 0x7ec1b4f1ac90 state=running>,
        <Future at 0x7ec1b4f46330 state=running>,  
        <Future at 0x7ec1b4f96720 state=pending>
    ]

    """

    """ 
    tast.result output in each round of loop execution

        ('https://stackoverflow.com/a', 404, 'url-valid')

    """
    

#There are a number of future objects inside the processes variable 
#future objects will not be processed according to their order
#Any future object that changes its status faster from running to done 
# then It will be processed faster 
#And all this is because we have used the as_completed function

    for task in as_completed(processes):  
        #print(task.result())
        if task.result()[2] == 'url-valid':
            status_group = str(task.result()[1])[0] + "xx"
            status_codes[status_group].append((task.result()[0], task.result()[1]))
        else:
            status_codes["Invalid"].append((task.result()[0], task.result()[1]))

"""

status_codes is a dictionary and be like 
    {
        '1xx': [],
        '2xx': [ ('http://www.google.com', 200), ('https://www.google.com', 200) ]
        '3xx': [], 
        '4xx': [  ('https://stackoverflow.com/a', 404), ('https://stackoverflow.com/b', 404) ], 
        '5xx': [], 
        'Invalid': [  ('https://asdf87as.com', 'not resolve to ip'), ('https://rocket.com', 'not resolve to ip')  ]
    }

"""



#If the status_codes.items() variable equal to  upper line 

#As a result, it returns a value similar to below line  ,  in each round of execution of the loop
#'2xx': [ ('http://www.google.com', 200), ('https://www.google.com', 200) ]


#In this case, the code variable  takes the value of '2xx'
#and urls variable  takes the value of [ ('http://www.google.com', 200), ('https://www.google.com', 200) ]

for code, urls in status_codes.items():
    if urls:
        print(COLORS.get(code, Fore.WHITE) + f'===== {code.upper()} =====')
        print("Number_Of_Urls_In_This_Group : " ,len(status_codes[code]))

        #If the urls variable equal to  [ ('http://www.google.com', 200), ('https://www.google.com', 200) ]

        #As a result, it returns a value similar to below line  ,  in each round of execution of the loop
        #('http://www.google.com', 200)

        #In this case, the url variable  takes the value of ' http://www.google.com  '
        #and status variable  takes the value of 200

        for url, status in urls:
            print(f'[Status : {status}] = {url}')
        print(Style.RESET_ALL)


