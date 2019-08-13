from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import csv
import re
import time

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):

    print(e)

movieTitles = []
ratings = []
genres = []
movies = []
budgets = []

directors = []
actor1 = []
actor2 = []

def getHtmlFromIMDB (url):
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    for c, content in enumerate(html.findAll("div", {"class", "lister-item-content"})):
        for i, h3 in enumerate(content.findAll("h3", {"class","lister-item-header"})):
            for z, titleMovie in enumerate(h3.findAll("a")):
                movieTitles.append(titleMovie.text)
        for i, rating in enumerate(content.findAll("div", {"class", "inline-block ratings-imdb-rating"})):
            rating = rating.text.replace('\n', '')
            ratings.append(rating)

        for i, genre in enumerate(content.findAll("span", {"class", "genre"})):
            genre = genre.text.split(', ')[0]
            genre = genre.replace('\n', '')
            genre = genre.strip()
            genres.append(genre)

        for x, directorActors in enumerate(content.findAll("p", {'class', ''})):
            values = list(directorActors.text.split(','))
            for i in range(len(values)):
                values[i] = values[i].replace('Director:', '')
                values[i] = values[i].replace('Directors:', '')
                values[i] = values[i].replace('\n', '')
                values[i] = values[i].replace('Stars:', '')
                values[i] = values[i].replace('|', '')
                values[i] = values[i].strip()
            valueAppended = values[0]
            valueAppended = values[0].split('    ')
            if len(values) >= 3:
                values.pop(0)
                values.insert(0, valueAppended[0])
                if len(valueAppended) == 2:
                    values.insert(0, valueAppended[1])
                else:
                    valueAppended2 = values.pop(1)
                    valueAppended2 = valueAppended2.split('     ')
                    if len(valueAppended2) == 2:
                        values.insert(1, valueAppended2[0])
                    else:
                        values.insert(1, valueAppended2[0])
                        valueAppended3 = values.pop(3)
                        valueAppended3 = valueAppended3.split('     ')
                        if len(valueAppended3) == 2:
                            valueAppended3.pop()
                            valueAppended3 = valueAppended3[0]
                            values.insert(2, valueAppended3)
                        else:
                            valueAppended3 = valueAppended3[0]
                            values.insert(2, valueAppended3)

                values[0] = values[0].strip()
                values = values[:3]
                directors.append(values[0])
                actor1.append(values[1])
                actor2.append(values[2])
            else:
                directors.append('none')
                actor1.append('none')
                actor2.append('none')


currentNum = 1


for x in range(25):
    getHtmlFromIMDB("https://www.imdb.com/search/title/?title_type=feature,tv_movie,short&release_date=2000-01-01,2019-08-04&user_rating=1,10.0&num_votes=5000,1000000000&count=250&langauges=en&start=" + str(currentNum) + "&ref_=adv_nxt")
    currentNum += 250



for i in range(len(movieTitles)):
    thisIteration = [movieTitles[i], ratings[i], genres[i], directors[i], actor1[i], actor2[i]]
    movies.append(thisIteration)

with open('movies2.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(movieTitles)):
        filewriter.writerow(movies[i])
