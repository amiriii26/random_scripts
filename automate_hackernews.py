from bs4 import BeautifulSoup
import requests
import datetime
import sqlite3

def send_msg(msg1, msg2):
    token = "2109415764:AAHl9LnT3ZkyLTsEYE5j258GGcgH7oGYGxA"
    chat_id = "1256010126"
    url_req = "https://api.telegram.org/bot"+ token +"/sendMessage" + "?chat_id=" + chat_id + "&text=" + msg1 + "\n" + msg2
    results = requests.get(url_req)
    #print(results.json())

source = requests.get("https://thehackernews.com/").text
soup = BeautifulSoup(source, "lxml")

conn = sqlite3.connect('thehackernews_test.db')
c = conn.cursor()

for post in soup.find_all("div", {"class": "body-post"}):
    headline = post.h2.text
    print(headline)

    description = post.find('div', {"class": "home-desc"}).text
    # print(description)

    links = post.find('a', {"class":"story-link"})['href']
    print(links)

    fetched_link_from_web = links


    date_post = post.find('div', {"class": "item-label"}).findNext('i').next_sibling

    today = datetime.datetime.now()
    today_date = today.date()
    today_formatted = today_date.strftime('%B %d, %Y')
    print(date_post)

    ids = 1

    if (date_post == today_formatted ):
        c.execute("SELECT rowid,link FROM posts WHERE link = ? ", (fetched_link_from_web,))

        req_to_db = c.fetchall()
        print("in db -> ", req_to_db)

        if not req_to_db: # check into req_to_db list whether there is a link or not
            print("[+] added to database")
            c.execute("INSERT INTO posts (id, header, link, date ) VALUES (?,?,?,?)", (ids, headline, links, date_post))
            send_msg(headline, links)
            conn.commit()
        else:
            print("already in database.")
    else:
        print("No Need to add, old post.")

    print('-------------')

conn.close()
