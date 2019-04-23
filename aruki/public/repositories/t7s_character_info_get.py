import re
import pymysql
import requests
from bs4 import BeautifulSoup


def get_url():
    '''
    get t7s character url
    :return:url_list    type:list
    '''
    #ready url's element
    url_start = 'http://t7s.jp/character/chara/'
    url_finish = '.html'
    url_num = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
    for num in range(10, 49):
        url_num.append(str(num))
    #get url_list
    url_list=[]
    for num in url_num:
        url = url_start + num + url_finish
        url_list.append(url)
    return url_list


def get_html(url_list):
    '''
    get html about character's information from url
    :param url_list:        a list include url about t7s character's information
    :return: html_list      type:list
    '''
    html_list=[]
    for url in url_list:
        html=requests.get(url)
        html_div=BeautifulSoup(html.text,'lxml')
        name_div=html_div.select('#page-top > div.wrap-main > section > div > div > div.chara-modal__name > div > h4 > img')
        birthday_div=html_div.select('#page-top > div.wrap-main > section > div > div > div.chara-modal__info > div.chara-modal__data > div > dl:nth-child(2) > dd')
        CV_div=html_div.select('#page-top > div.wrap-main > section > div > div > div.chara-modal__info > div.chara-modal__data > div > dl:nth-child(6) > dd')
        age_div=html_div.select('#page-top > div.wrap-main > section > div > div > div.chara-modal__info > div.chara-modal__data > div > dl:nth-child(1) > dd')
        nickname_div=html_div.select('#page-top > div.wrap-main > section > div > div > div.chara-modal__info > div.chara-modal__data > div > dl:nth-child(7) > dd')
        blood_div=html_div.select('#page-top > div.wrap-main > section > div > div > div.chara-modal__info > div.chara-modal__data > div > dl:nth-child(3) > dd')
        HW_div=html_div.select('#page-top > div.wrap-main > section > div > div > div.chara-modal__info > div.chara-modal__data > div > dl:nth-child(4) > dd')
        BWH_div=html_div.select('#page-top > div.wrap-main > section > div > div > div.chara-modal__info > div.chara-modal__data > div > dl:nth-child(5) > dd')
        stunt_div=html_div.select('#page-top > div.wrap-main > section > div > div > div.chara-modal__info > div.chara-modal__data > div > dl:nth-child(8) > dd')
        like_div=html_div.select('#page-top > div.wrap-main > section > div > div > div.chara-modal__info > div.chara-modal__data > div > dl:nth-child(9) > dd')
        affiliate_div=html_div.select('#page-top > div.wrap-main > section > div > div > div.chara-modal__info > div.chara-modal__data > div > dl:nth-child(10) > dd')
        unit_div=html_div.select('#page-top > div.wrap-main > section > div > div > div.chara-modal__info > div.chara-modal__data > div > dl:nth-child(11) > dd')
        intro_div=html_div.select('#page-top > div.wrap-main > section > div > div > div.chara-modal__info > div.chara-modal__txt > p')
        #append into html_list
        list={'name':name_div[0],'birthday':birthday_div[0],'blood':blood_div[0],'HW':HW_div[0],'BWH':BWH_div[0], 'CV':CV_div[0],'nickname':nickname_div[0],
              'stunt':stunt_div[0],'like':like_div[0],'affiliate':affiliate_div[0],'unit':unit_div[0],'intro':intro_div[0]}
        html_list.append(list)
    return html_list


def get_date(html_list):
    '''
    get character's information date's dictionary from html
    :param html_list:   a list include html about name,birthdat,CV
    :return: date       type:dictionary
    '''
    date={}
    name_text='<img alt="(.*?)" src="'
    birthday_text='<dd class="chara-modal-data__cont">(.*?)</dd>'
    blood_text='<dd class="chara-modal-data__cont">(.*?)</dd>'
    HW_text='<dd class="chara-modal-data__cont">(.*?)</dd>'
    BWH_text='<dd class="chara-modal-data__cont">(.*?)</dd>'
    CV_text='<dd class="chara-modal-data__cont">(.*?)</dd>'
    nickname_text='<dd class="chara-modal-data__cont">(.*?)</dd>'
    stunt_text='<dd class="chara-modal-data__cont">(.*?)</dd>'
    like_text='<dd class="chara-modal-data__cont">(.*?)</dd>'
    affiliate_text='<dd class="chara-modal-data__cont">(.*?)</dd>'
    unit_text='<dd class="chara-modal-data__cont">(.*?)</dd>'
    intro_text='<p>(.*?)</p>'
    #date cleansing
    for character in html_list:
        name=re.findall(name_text,str(character['name']))[0]
        birthday=re.findall(birthday_text,str(character['birthday']))[0]
        blood=re.findall(blood_text,str(character['blood']))[0]
        HW=re.findall(HW_text,str(character['HW']))[0]
        BWH=re.findall(BWH_text,str(character['BWH']))[0]
        CV=re.findall(CV_text,str(character['CV']))[0]
        nickname=re.findall(nickname_text,str(character['nickname']))[0]
        stunt=re.findall(stunt_text,str(character['stunt']))[0]
        like=re.findall(like_text,str(character['like']))[0].replace('\u3000',' and ')
        affiliate=re.findall(affiliate_text,str(character['affiliate']))[0]
        unit=re.findall(unit_text,str(character['unit']))[0]
        intro=re.findall(intro_text,str(character['intro']))[0]
        information={'birthday':birthday,'blood':blood,'HW':HW,'BWH':BWH,'CV':CV,'nickname':nickname,
                     'stunt':stunt,'like':like,'affiliate':affiliate,'unit':unit,'intro':intro}
        date[name]=information;
    return date


def start():
    url_list=get_url()
    html_list=get_html(url_list)
    date=get_date(html_list)
    return date

def jsonget(date):
    import json
    date_json=json.dumps(date)
    with open("E:/Python/Python3 work-file/character_information.json",'w',encoding='utf-8') as f:
        f.write(date_json)

def mysql(date):
    '''
    select date into mysql
    :param date:
    :return:
    '''
    connect=pymysql.Connect(
        host="localhost",
        port= 3306,
        user="root",
        password="ARUKIONEjiebin22",
        db="t7s",
        charset="utf8"
    )
    character=connect.cursor()
    for menber in date.keys():
        insert='insert into character_information value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        character.execute(insert,
                          (menber,
                          date[menber]['birthday'],
                          date[menber]['blood'],
                          date[menber]['HW'],
                          date[menber]['BWH'],
                          date[menber]['CV'],
                          date[menber]['nickname'],
                          date[menber]['stunt'],
                          date[menber]['like'],
                          date[menber]['affiliate'],
                          date[menber]['unit'],
                          date[menber]['intro'])
        )
        connect.commit()
    character.close()
    connect.close()


date=start()
mysql(date)
