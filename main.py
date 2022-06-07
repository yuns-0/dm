import os, json, random, threading, requests, time, instagrapi, traceback, os, pymongo, subprocess
from tabnanny import check
from instagrapi import Client
from bs4 import BeautifulSoup
import asyncio
from proxybroker import Broker


__PROGRAMID__ = "c2JedU7LcPNfkW8H9yPVAFjTuPxeJh9"
__VERSION__ = "1.1"

config = json.loads(open("./config.json", "r", encoding="utf-8").read())


class color:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET_ALL = "\033[0m"
    BLUE = '\033[96m'






async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, 'a') as f:
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            row = '%s:%d\n' % (proxy.host, proxy.port)
            try:
                f.write(row)
            except:
                pass


def get_proxies():
    print("get proxies")
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find(types=['HTTPS'], limit=10),
                           save(proxies, filename='proxies.txt'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)


def user_handler():
    with open("./usernames.txt", encoding="utf-8") as f:
        lines = f.readlines()
        tokens = []
        for splines in lines:
            hdr = splines.split("\n")[0]
            tokens.append(hdr)
    return tokens


def name_handler():
    with open("./names.txt", encoding="utf-8") as f:
        lines = f.readlines()
        tokens = []
        for splines in lines:
            hdr = splines.split("\n")[0]
            tokens.append(hdr)
    return tokens


def send_dm(username, password, proxy, userdm, messageText, count, i):
    try:
        username = username
        password = password
        cl = Client()
        if config["script_settings"]["use_proxy"]:
            cl.set_proxy(proxy["https"])
        cl.login(username, password)
        userid = cl.user_id_from_username(userdm)
        print(userid)
        for x in range(0,count):
            a = cl.direct_send(messageText, [int(userid)])
            print(f"{color.GREEN}[{i}] {color.RESET_ALL}Message succesfully sent to {color.GREEN}@{userdm} {color.RESET_ALL}with {color.GREEN}@{username}{color.RESET_ALL}.")
    except Exception as err:
        print(f"{color.RED}[{i}]{color.RESET_ALL} An error occured when sending message to {color.RED}@{userdm} {color.RESET_ALL}account. Passing. ERROR: {err}")
        #traceback.print_exc()
        pass


def start(thread):

    try:
        tx = []
        names = name_handler()
                    
        for id, user_name in enumerate(user_handler()):
            ts = random.randint(35,50)
            print(f"please wait {ts}s .....")
            time.sleep(ts)
            if (id+1)%4==0:
                get_proxies()
                ts = random.randint(60,180)
                print(f"please wait {ts}s .....")
                time.sleep(ts)
            pp = None
            proxies = open("./proxies.txt", "+r", encoding="utf-8").read().splitlines()
            while pp is None:
                try:
                    prox = {"http": f"http://{random.choice(proxies)}", "https": f"{config['script_settings']['proxy_type']}://{random.choice(proxies)}"}
                    a = requests.get("http://ip-api.com/json/", proxies=prox, timeout=7, verify=False)
                    pp = prox
                    print(f"{color.GREEN}[{id+1}] Proxy is working. IP: {a.json()['query']} | COUNTRY: {a.json()['country']} {color.RESET_ALL}")
                except:
                    print(f"{color.RED}[{id+1}] Bad proxy. {prox['https']}")
                    pass

            if config["script_settings"]["use_proxy"]:
                                
                if threading.active_count() <= thread:
                    print("ok")
                    a = requests.get("http://ip-api.com/json/", proxies=prox, timeout=7, verify=False)
                    print(f"{color.GREEN}[{id+1}] Proxy is working. IP: {a.json()['query']} | COUNTRY: {a.json()['country']} {color.RESET_ALL}")
                    text_message = config["instagram_settings"]["text_message"]
                    mT = threading.Thread(target=send_dm, args=(config["instagram_settings"]["username"],config["instagram_settings"]["password"], pp, user_name, text_message,config["script_settings"]["message_amount"],id+1))
                    #send_dm(config["instagram_settings"]["username"],config["instagram_settings"]["password"], random.choice(working_proxies), user_name, config["instagram_settings"]["text_message"])
                    mT.daemon = True
                    mT.start()
                    tx.append(mT)
            else:
                if threading.active_count() <= thread:
                    name = names[id] 
                    if name == "Hey":
                        name = user_name
                    print(f"Start send to {color.YELLOW}@{user_name} {color.RESET_ALL}")
                    text_message =  f"""Hey {name},We do brand deals with different companies like Tinder, Bumble, etc. Are you interested in doing paid promos?"""
                    mT = threading.Thread(target=send_dm, args=(config["instagram_settings"]["username"],config["instagram_settings"]["password"], None, user_name, text_message,config["script_settings"]["message_amount"],id+1))
                    #send_dm(config["instagram_settings"]["username"],config["instagram_settings"]["password"], random.choice(working_proxies), user_name, config["instagram_settings"]["text_message"])
                    mT.daemon = True
                    mT.start()
                    tx.append(mT)
        
        
        for t in tx:
            t.join(75)
    except Exception as e:
        traceback.print_exc()
        pass


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    check = [True]
    if check[0]:   
        print(f"{color.GREEN}[+] License correct program starting... {color.RESET_ALL}")
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")
        print(fr"""{color.GREEN}         
                                            )  
                (       (                 ( /(  
                )\ )   ))\   (     (      )\()) 
                (()/(  /((_)  )\ )  )\    ((_)\  
                )(_))(_))(  _(_/( ((_)   /  (_) 
                | || || || || ' \))(_-< _| () |  
                \_, | \_,_||_||_| /__/(_)\__/   
                |__/                            

                Press any key to start the script...
                {color.RESET_ALL}    """)

        input("....")

        try:
            get_proxies()
            start(config["script_settings"]["threading"])
            input("....")
            
        except:
            traceback.print_exc()
            input(".....")
    else:
        print(f"{color.RED}[-] {check[1]} {color.RESET_ALL}")
        input("....")
