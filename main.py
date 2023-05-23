import requests
import time
from seleniumwire  import webdriver
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
}

def new_cookies():
    new_cookies_sel = {}
    try:
        driver.get("https://tik9.spbik.spb.ru/index.php?p=2")
        time.sleep(2)
        for i in driver.get_cookies():
            key = i.get("name")
            name = i.get("value")
            new_cookies_sel[key] = name
    except Exception as  ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
    cookies_db1 = {
        "accept": new_headers['accept'],
        'user-agent': new_headers['user-agent'],
        "cookie": f'_ym_isad={new_cookies_sel.get("_ym_isad")}; '
                  f'_ym_d={new_cookies_sel.get("_ym_d")}; '
                  f'_ym_uid={new_cookies_sel.get("_ym_uid")}; '
                  f'sputnik_session={new_cookies_sel.get("sputnik_session")}; '
                  f'sp_test={new_cookies_sel.get("sp_test")}; '
    }

    return {"cookies":cookies_db1, 'headers':new_headers}

def find_class(code, cookies, headers):
    result = {}
    listpeople =[]
    try:
        link = f"https://tik{code}.spbik.spb.ru/index.php?p=2"
        response = requests.get(link, headers=headers, cookies=cookies)
        soup = BeautifulSoup(response.content, 'html.parser')
        tr = soup.find_all("tr")
        tagb = soup.find_all("b")
        div_name_com = soup.find_all("div")
        for val in tagb:
            if val.get_text().startswith("Состав"):
                nametik=val.get_text()
                listpeople.append(nametik)
                break
            else:
                for ii in div_name_com:
                    if ii.get_text().startswith("Состав"):
                        nametik = ii.get_text()
                        listpeople.append(nametik)
                        break
            break

        for td in tr:
            if len(td) == 3:
                threlist = []
                for i in td:
                    try:
                        if i.attrs.get('class') == None:
                            value = i.get_text()
                            threlist.append(value)
                    except:
                        value = i.get_text()
                        threlist.append(value)
                if threlist != []:
                    listpeople.append(threlist)
            else:
                twolist = []
                for i in td:
                    try:
                        if i.attrs.get('class') == None:
                            value = i.get_text()
                            twolist.append(value)
                    except:
                        value = i.get_text()
                        twolist.append(value)
                if twolist != []:
                    listpeople.append(twolist)

    except Exception as e:
        print(e)
        print(f"Упаили с исключением на участке {code}")

    result[code] = listpeople
    print(result)
    return result


def append_file( namefile: str, nametik:str, listpeople :list ):
    with open(namefile, 'a', newline='',encoding="utf-8" ) as f_object:
        writer_object = writer(f_object, dialect='excel')
        writer_object.writerow([nametik])
        writer_object.writerows(listpeople)
        f_object.close()


if __name__== "__main__":
    data = datetime.datetime.now().strftime("%Y_%m_%d_%M_%S")
    filename = f"{data}_{SAVEFILE}"
    web = new_cookies()
    file = open(filename, 'w', encoding='UTF8')
    file.close()
    for i in range(1,TIK):
        time.sleep(1)
        res = find_class(i, web.get("cookies"), web.get("headers"))
        append_file( filename, res.get(i)[0], res.get(i)[1:] )


