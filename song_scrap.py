import requests
from bs4 import BeautifulSoup
import os

import pandas as pd
import re

#--------------------------------------------------------------------------------
def actor_page_get(url = None,file_name = None):
    '''
    method to create text file which will have hyper links
    of all movies of an actor
    '''
    try:
        req = requests.get(url).text
        # Parse the html content

        soup = BeautifulSoup(req, "lxml")
        song_area = soup.find("div",attrs={"class":"entry-content"})
        required_links = song_area.find_all("a")
        required_links = required_links[:-4]
        required_links = required_links[7:]
        fd = open(file = 'movies_list_allu_arjun.txt',mode = 'w+',encoding="utf8", errors ='ignore')
        for i in required_links:
            fd.write(str(i) + '\n')
        fd.close
        print('--completed--')
    except Exception as e:
        print(f'exception occured in step 1 {e}')

#---------------------------------------------------------------------------------
def title_separate(x):
    '''method to separate the title name from raw text'''
    try:
        regex = r"\btitle(.*)\""
        result = re.findall(regex,x)
        return result[0].lstrip('="')
    except Exception as e:
        pass

def url_separate(x):
    '''method to separate movie url from raw text '''
    try:
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        result = re.findall(regex,x)
        return result[0][0]
    except Exception as e:
        print(f'exception occured in step 2 url separation {e}')
        pass

def movie_page_get(url):
    '''
    method to navigate movie page and grab song urls
    '''
    try:
        req = requests.get(url).text
        soup = BeautifulSoup(req, "lxml")
        song_area = soup.find("div",attrs={"class":"entry-content"})
        required_links = song_area.find_all("a",attrs = {"rel":"nofollow"})
        results = [url_separate(str(i)) for i in required_links]
        return results
    except Exception as e:
        print(f'exception occured in step 2 song_urls get {e}')
        pass

def get_song_name(song_url):
    '''method to get song_name from song url'''
    try:
        song_name = song_url.split('/')[-1]
        return song_name
    except Exception as e:
        print(f'exception occured in step 2 song_urls get {e}')
        pass

def song_download(song_urls):
    '''method to download song '''
    try:
        for i in song_urls:
            download = requests.get(i)
            file_name = get_song_name(i)
            #print(download.headers)
            #filename = getFilename_fromCd(download.headers.get('content-disposition'))
            if download.status_code == 200:
                with open('songs/'+ file_name, 'wb') as f:
                    f.write(download.content)
            else:
                print(f"Download Failed For File {file_name}")
    except Exception as e:
        print(f'exception occured in step 3 song_download get {e}')
        pass


#----------------------------------------------------------------------------------

#--------------step 1---------------#
url = 'https://sensongsmp3.tv/allu-arjun/'
file_name = 'movies_list_allu_arjun.txt'
actor_page_get(url = url, file_name = file_name)
#-------------step 2---------------#
movies_df = pd.read_csv(file_name, names = ['movies_urls'])

#url separation
movies_df['url_links'] = movies_df['movies_urls'].apply(url_separate)

#movie title separation
movies_df['movie_name'] = movies_df['movies_urls'].apply(title_separate)

#movie songs urls extraction
movies_df['song_urls'] = movies_df['url_links'].apply(movie_page_get)
#movies_df['total_songs'] = movies_df['song_urls'].apply(len)

# movies songs dowloading process
movies_df['song_urls'].apply(song_download)

#----------------------------------------------------------------------------------
'''
final songs are downloaded in file folder called songs and be cautious
all songs are mixed in the folder and there are no subfolders by movie title name
'''