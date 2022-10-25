import imp
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from konlpy.tag import Okt
import openpyxl

# options = webdriver.ChromeOptions()
# options.add_argument("disable-gpu")  # 그래픽 성능 낮춰서 크롤링 성능 쪼금 높이기
# options.add_argument(
#     "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")  # 네트워크 설정
# options.add_argument("lang=ko_KR")  # 사이트 주언어
# driver = webdriver.Chrome(
#     "/Users/park/Desktop/Assignment/IT집중교육/project/chromedriver")

# data_list = []
# max_iter = 10
# url_list = []
# # url = "https://www.youtube.com/c/UPKTV/videos"
# url = "https://www.youtube.com/"


def scroll_down():
    driver.get(url)
    last_page_height = driver.execute_script(
        "return document.documentElement.scrollHeight")
    i = 0
    while i < max_iter:
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2.5)
        i += 1
        new_page_height = driver.execute_script(
            "return document.documentElement.scrollHeight")
        if new_page_height == last_page_height:
            break


def find_url():
    scroll_down()
    html0 = driver.page_source
    html = BeautifulSoup(html0, 'html.parser')
    # video_url_list = html.findAll('a', {'id': 'video-title'})
    video_url_list = html.findAll('a', {'id': 'video-title-link'})
    for a in video_url_list:
        # url_list.append('https://www.youtube.com' + a.attrs['href'])
        if a.get('href') is not None:
            url_list.append('https://www.youtube.com' + a.get('href'))


def main():
    find_url()
    print("Total Length = " + " ", len(url_list))
    for idx in range(len(url_list)):
        print("iter = ", idx + 1)
        driver.get(url_list[idx])
        last_page_height = driver.execute_script(
            "return document.documentElement.scrollHeight")
        i = 0
        while i < max_iter:
            driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            i += 1
            new_page_height = driver.execute_script(
                "return document.documentElement.scrollHeight")
            if new_page_height == last_page_height:
                break

        html0 = driver.page_source
        html = BeautifulSoup(html0, 'html.parser')
        comments_list = html.findAll(
            'ytd-comment-thread-renderer', {'class': 'style-scope ytd-item-section-renderer'})

        for j in range(len(comments_list)):
            comment = comments_list[j].find(
                'yt-formatted-string', {'id': 'content-text'}).text
            comment = comment.replace('\n', '')  # 줄 바뀜 없애기
            comment = comment.replace('\t', '')  # 탭 줄이기

            data = {'comment': comment}
            data_list.append(data)

        result_df = pd.DataFrame(data_list, columns=['comment'])
        result_df.to_excel(
            f'/Users/park/Desktop/Assignment/IT집중교육/project/comment_youtube.csv', index=False)
    driver.close()


def wort_to_vector():
    df = pd.read_excel('comment_youtube_2.xlsx')
    print(df.head())
    print(df.shape)


# main()
wort_to_vector()
