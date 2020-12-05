from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import sqlite3 , csv
from sqlite3 import Error


''' #creating sqlite db for storing all the information about videos so that we can upload the data to the google sheets
def creation_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
if __name__ == '__main__':
    creation_connection(r"C:\sqlite\db\pythonsqlite.db")
'''
#ask for month and the year and also how many pages of result you want to fetch
month =str(input("Please put in month of the result you want: "))
year = str(input("Please put in full year of the result you want: "))
pages = int(input("Please put in how many number of pages you want: "))

#grabs all the href for all the videos and puts it into a list
all_links = []
all_views = []
all_ratings = []



for i in range(pages):
    requested_url = 'MediaWebsiteLink' + year + '-' + month + '/' + str(i)
    uClient = uReq(requested_url)
    page_html = uClient.read()
    uClient.close()

    soup_page = soup(page_html, 'html.parser')
    videos = soup_page.find_all("p", {'class': 'title'})

    #links of all href in a list
    videolinks = [video.a for video in videos]

    for links in videolinks:
        all_links.append(links['href'])


#opening a new csv line, setting up the field names on a new row
with open('mycsv.csv', 'w', newline='') as f:
    fieldnames = ['Link','Views', 'Thumbs Up', 'Thumbs Down']
    thewriter = csv.DictWriter(f, fieldnames = fieldnames)
    thewriter.writeheader()
#loop through all the links in the video and grab their likes and views
    for eachvideo in all_links:
        requested_url_foreach_video = 'MediaWebsiteLink'+ eachvideo
        uClient = uReq(requested_url_foreach_video)
        page_html = uClient.read()
        uClient.close()

        soup_page2 = soup(page_html, 'html.parser')
        #number of views
        video_page_views = soup_page2.find("strong", {"id": "nb-views-number"})
        #this gets the thumbs up value
        rating_thumbsup = soup_page2.find("a", {"class": "btn btn-default vote-action-good"})
        #for thumbs down
        rating_thumbsdn = soup_page2.find("a", {"class": "btn btn-default vote-action-bad"})
        #This writes all the data to the CSV file
        thewriter.writerow({'Link': eachvideo , 'Views':video_page_views.text , 'Thumbs Up': rating_thumbsup.text , 'Thumbs Down': rating_thumbsdn.text})


print(all_links)