import datetime
import requests
from bs4 import BeautifulSoup

SCRAPER_MAILGUN_API = "XXX"
SCRAPER_MAILGUN_DOMAIN = "XXX"
SCRAPER_MAILGUN_FROM = "XXX"
SCRAPER_MAILGUN_TO = "XXX"


class Movie:
  desc = ""
  def __init__(self, movieId, title, url):
    self.movieId = movieId
    self.title = title
    self.url = url
  def getDBString(self):
    return self.movieId + " - " + self.title
  

# Current movies
def getMovies():
  try:
    page = requests.get("https://www.pathe.nl/films/actueel")
  except:
    writeToLog("Fout bij openen URL door requests.get", True)

  soup = BeautifulSoup(page.content, "html.parser")
  movieElements = soup.find_all("a", class_="poster")
  if len(movieElements) < 1:
    writeToLog("Beautifulsoup heeft geen film elementen gevonden op de pagina", True)

  movies = []
  for movieElement in movieElements:

    movieId = movieElement.get('data-gtmclick')
    if(movieId == None):
      writeToLog("Kan movieId niet ophalen", True)


    t = movieElement.find("p", class_="poster__label")
    if(t == None):
      writeToLog("Kan titel niet ophalen", True)
    else:
      title = t.text

    url = "https://www.pathe.nl" + movieElement.get('href')
    if(url == None):
      writeToLog("Kan url niet ophalen", True)
    
    newMovie = Movie(movieId, title, url)
    movies.append(newMovie)

  return movies


def checkDB(movies):
  f = open("database.txt", "r")
  db = f.read().splitlines()
  f.close()

  newMovies = []
  for movie in movies:
    if(movie.getDBString() not in db):
      page = requests.get(movie.url)
      soup = BeautifulSoup(page.content, "html.parser")
      desc1 = soup.find('span', itemprop="description")
      desc2 = soup.find('span', class_="js-toggle-text")
      if desc1:
        movie.desc = desc1.text
        if desc2:
          movie.desc += desc2.text
      else:
        writeToLog("Kan omschrijving van film niet ophalen", True)
      newMovies.append(movie)
    
  return newMovies

def createMail(movies):
  mail = "Dit zijn de nieuwe films:\n\n"
  for movie in movies:
    mail += "***" + movie.title + "***\n"
    mail += movie.desc
    mail += "\n-------------------------------------------------\n"

  
  mailResult = requests.post(
        "https://api.eu.mailgun.net/v3/%s/messages"%SCRAPER_MAILGUN_DOMAIN,
        auth=("api", SCRAPER_MAILGUN_API),
        data={"from": "Pathe scraper <%s>"%SCRAPER_MAILGUN_FROM,
              "to": SCRAPER_MAILGUN_TO,
              "subject": "Nieuwe films",
              "text": mail})
  
  if mailResult.status_code == 200:
    file = open("database.txt", "a")
    for movie in movies:
      file.write(movie.getDBString() + "\n")
    file.close()
    writeToLog("Klaar", False)
  else:
    writeToLog("Mail kon niet worden verstuurd", True)

def writeToLog(text, isError):
  logFile = open("log.txt", "a")
  logFile.write("Time: %s ---> %s \n"%(datetime.datetime.now(), text))
  logFile.close()
  if isError:
    print("Error, see log")
    exit()

movies = getMovies()
newMovies = checkDB(movies)

if(len(newMovies) > 0):
  createMail(newMovies)
else:
  writeToLog("Geen nieuwe films gevonden", False)