import requests
import time
from seleniumwire  import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from config import TIK, PATHCHROME, SAVEFILE
import csv
from csv import writer
import datetime

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--hide-scrollbars')
options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
driver = webdriver.Chrome(executable_path=PATHCHROME, options=options)

new_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Referer":"http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ik&vrn=4784001382675"
}

def new_cookies():
    new_cookies_sel = {}
    tik_num_list = []
    res_tik_dict_uch = {}
    try:
        print("Сейчас идет сбор данных о ТИКах и УИКах. Увлекательное путешествие займет около 30 миниут. ")
        driver.get("http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ik")
        tik_number = driver.find_elements(By.TAG_NAME, "li")
        for num in tik_number:
            tik_num_list.append(num.get_attribute("id"))

        for name_tik in tik_num_list[1:]:
            driver.get(f"http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ik&vrn={name_tik}")
            uchnumber = driver.find_elements(By.TAG_NAME, "li")
            res_tik_dict_uch[name_tik] = []
            for get_uch in uchnumber:
                if get_uch.get_attribute("id") not in tik_num_list:
                    res_tik_dict_uch.get(name_tik).append(get_uch.get_attribute("id"))

        for i in driver.get_cookies():
            key = i.get("name")
            name = i.get("value")
            new_cookies_sel[key] = name
        print(new_cookies_sel)

    except Exception as  ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
    cookies_db1 = {
        "accept": new_headers['accept'],
        'user-agent': new_headers['user-agent'],
        "cookie": f'izbFP={new_cookies_sel.get("izbFP")}; '
                  f'session-cookie={new_cookies_sel.get("session-cookie")}; '
                  f'sputnik_session={new_cookies_sel.get("sputnik_session")}; '
                  f'izbSession={new_cookies_sel.get("izbSession")}; '
                  f'JSESSIONID={new_cookies_sel.get("JSESSIONID")}; '
    }

    return {  'headers':cookies_db1,  "result":res_tik_dict_uch }

def append_file( namefile: str, nametik:str, listpeople :list ):
    with open(namefile, 'a', newline='',encoding="utf-8" ) as f_object:
        writer_object = writer(f_object, dialect='excel')
        writer_object.writerow([nametik])
        writer_object.writerows(listpeople)
        f_object.close()


def find_class(code, headers ):
    result = {}
    listpeople = []
    try:
        link = f"http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ik&vrn={code}"
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        h2 = soup.find_all("h2")
        tr = soup.find_all("tr")
        for hh in h2:
            if hh.get_text().startswith("Санкт-Петербургская") or hh.get_text().startswith("ТИК ") \
                    or hh.get_text().startswith("Участковая"):
                nametik = hh.get_text()
                listpeople.append(nametik)
                break
        for td in tr:
            threlist = []
            for i in td:
                if not i.get_text().startswith('\n'):
                    if i.get_text() != '':
                        threlist.append(i.get_text())
            if threlist != []:
                listpeople.append(threlist)

    except Exception as e:
        print(e)
        print(f"Упаили с исключением")

    result[code] = listpeople
    print(result)
    return result




if __name__== "__main__":
    # web = new_cookies()
    # find_class( web.get("headers"), web.get("result"))
    data = datetime.datetime.now().strftime("%Y_%m_%d_%M_%S")
    filename = f"{data}_{SAVEFILE}"
    web = new_cookies()
    file = open(filename, 'w', encoding='UTF8')
    file.close()

    for parse in web.get("result").keys():
        time.sleep(1)
        res = find_class(parse, web.get("headers"))
        append_file(filename, res.get(parse)[0], res.get(parse)[1:])
        for par in web.get("result").get(parse):
            time.sleep(1)
            res = find_class(par, web.get("headers"))
            append_file(filename, res.get(par)[0], res.get(par)[1:])





