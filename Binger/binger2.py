import os
from os import system, name
import json

# precheck for the installation of files
def preCheck():
    libraries = ["pyfiglet","requests","requests_cache","bs4","pyfiglet","termcolor"]
    try:
        config = json.load(fp=open('binger.config'))
        for library in libraries:
            if library not in config:
                os.system("pip install "+library)
                config[library] = True
            elif config[library] != True:
                os.system("pip install "+library)
                config[library] = True
        if "webtorrent" not in config:
            os.system("npm install -g webtorrent")
            config["webtorrent"] = True
        elif config["webtorrent"] != True:
            os.system("npm install -g webtorrent")
            config["webtorrent"] = True
        json.dump(config, fp=open('binger.config', 'w'))
    except Exception as e:
        print(e)
        config = {}
        for i in libraries:
            os.system("pip install "+i)
            config[i]=True
        os.system("npm install -g webtorrent")
        config["webtorrent"]=True
        json.dump(config, fp=open('binger.config', 'w'))

print("Checking for updates...")
print("Checking for the libraries installed or not...")

preCheck() # precheck for the installation of files

# load the libraries post precheck
import pyfiglet
import termcolor
import requests
import requests_cache
from bs4 import BeautifulSoup
import webbrowser

# py1337x for the request module for 1337x
class py1337x():
    def __init__(self, proxy=None, cookie=None, cache=None, cacheTime=86400, backend='sqlite'):
        self.baseUrl = f'https://www.{proxy}' if proxy else 'https://www.1377x.to'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.5',
            'upgrade-insecure-requests': '1',
            'te': 'trailers'
        }

        if cookie:
            self.headers['cookie'] = f'cf_clearance={cookie}'

        self.requests = requests_cache.CachedSession(cache, expire_after=cacheTime, backend=backend) if cache else requests

    #: Searching torrents
    def search(self, query, page=1, category=None, sortBy=None, order='desc'):
        query = '+'.join(query.split())
        category = category.upper() if category and category.lower() in ['xxx', 'tv'] else category.capitalize() if category else None
        url = f"{self.baseUrl}/{'sort-' if sortBy else ''}{'category-' if category else ''}search/{query}/{category+'/' if category else ''}{sortBy.lower()+'/' if sortBy else ''}{order.lower()+'/' if sortBy else ''}{page}/"

        response = self.requests.get(url, headers=self.headers)
        return torrentParser(response, baseUrl=self.baseUrl, page=page)

    #: Trending torrents
    def trending(self, category=None, week=False):
        url = f"{self.baseUrl}/trending{'-week' if week and not category else ''}{'/w/'+category.lower()+'/' if week and category else '/d/'+category.lower()+'/' if not week and category else ''}"

        response = self.requests.get(url, headers=self.headers)
        return torrentParser(response, baseUrl=self.baseUrl)

    #: Top 100 torrents
    def top(self, category=None):
        category = 'applications' if category and category.lower() == 'apps' else 'television' if category and category.lower() == 'tv' else category.lower() if category else None
        url = f"{self.baseUrl}/top-100{'-'+category if category else ''}"

        response = self.requests.get(url, headers=self.headers)
        return torrentParser(response, baseUrl=self.baseUrl)

    #: Popular torrents
    def popular(self, category, week=False):
        url = f"{self.baseUrl}/popular-{category.lower()}{'-week' if week else ''}"

        response = self.requests.get(url, headers=self.headers)
        return torrentParser(response, baseUrl=self.baseUrl)

    #: Browse torrents by category type
    def browse(self, category, page=1):
        category = category.upper() if category.lower() in ['xxx', 'tv'] else category.capitalize()
        url = f'{self.baseUrl}/cat/{category}/{page}/'

        response = self.requests.get(url, headers=self.headers)
        return torrentParser(response, baseUrl=self.baseUrl, page=page)

    #: Info of torrent
    def info(self, link=None, torrentId=None):
        if not link and not torrentId:
            raise TypeError('Missing 1 required positional argument: link or torrentId')
        elif link and torrentId:
            raise TypeError('Got an unexpected argument: Pass either link or torrentId')

        link = f'{self.baseUrl}/torrent/{torrentId}/h9/' if torrentId else link
        response = self.requests.get(link, headers=self.headers)

        return infoParser(response, baseUrl=self.baseUrl)

# parser for the torrents
def torrentParser(response, baseUrl, page=1):
    soup = BeautifulSoup(response.content, 'html.parser')

    torrentList = soup.select('a[href*="/torrent/"]')
    seedersList = soup.select('td.coll-2')
    leechersList = soup.select('td.coll-3')
    sizeList = soup.select('td.coll-4')
    timeList = soup.select('td.coll-date')
    uploaderList = soup.select('td.coll-5')

    lastPage = soup.find('div', {'class': 'pagination'})

    if not lastPage:
        pageCount = page
    else:
        try:
            pageCount = int(lastPage.findAll('a')[-1]['href'].split('/')[-2])

        except Exception:
            pageCount = page

    results = {
        'items': [],
        'currentPage': page or 1,
        'itemCount': len(torrentList),
        'pageCount': pageCount
    }

    if torrentList:
        for count, torrent in enumerate(torrentList):
            name = torrent.getText().strip()
            torrentId = torrent['href'].split('/')[2]
            link = baseUrl+torrent['href']
            seeders = seedersList[count].getText()
            leechers = leechersList[count].getText()
            size = sizeList[count].contents[0]
            time = timeList[count].getText()
            uploader = uploaderList[count].getText().strip()
            uploaderLink = baseUrl+'/'+uploader+'/'

            results['items'].append({
                'name': name,
                'torrentId': torrentId,
                'link': link,
                'seeders': seeders,
                'leechers': leechers,
                'size': size,
                'time': time,
                'uploader': uploader,
                'uploaderLink': uploaderLink
            })

    return results

# information parser for the torrents
def infoParser(response, baseUrl):
    soup = BeautifulSoup(response.content, 'html.parser')

    name = soup.find('div', {'class': 'box-info-heading clearfix'})
    name = name.text.strip() if name else None

    shortName = soup.find('div', {'class': 'torrent-detail-info'})
    shortName = shortName.find('h3').getText().strip() if shortName else None

    description = soup.find('div', {'class': 'torrent-detail-info'})
    description = description.find('p').getText().strip() if description else None

    genre = soup.find('div', {'class': 'torrent-category clearfix'})
    genre = [i.text.strip() for i in genre.find_all('span')] if genre else None

    thumbnail = soup.find('div', {'class': 'torrent-image'})
    thumbnail = thumbnail.find('img')['src'] if thumbnail else None

    if thumbnail and not thumbnail.startswith('http'):
        thumbnail = f'{baseUrl}'+thumbnail

    magnetLink = soup.select('a[href^="magnet"]')
    magnetLink = magnetLink[0]['href'] if magnetLink else None

    infoHash = soup.find('div', {'class': 'infohash-box'})
    infoHash = infoHash.find('span').getText() if infoHash else None

    images = soup.find('div', {'class': 'tab-pane active'})
    images = [i['src'] for i in images.find_all('img')] if images else None

    descriptionList = soup.find_all('ul', {'class': 'list'})

    if len(descriptionList) > 2:
        firstList = descriptionList[1].find_all('li')
        secondList = descriptionList[2].find_all('li')

        category = firstList[0].find('span').getText()
        species = firstList[1].find('span').getText()
        language = firstList[2].find('span').getText()
        size = firstList[3].find('span').getText()
        uploader = firstList[4].find('span').getText().strip()
        uploaderLink = baseUrl+'/'+uploader+'/'

        downloads = secondList[0].find('span').getText()
        lastChecked = secondList[1].find('span').getText()
        uploadDate = secondList[2].find('span').getText()
        seeders = secondList[3].find('span').getText()
        leechers = secondList[4].find('span').getText()

    else:
        category = species = language = size = uploader = uploaderLink = downloads = lastChecked = uploadDate = seeders = leechers = None

    return {
        'name': name,
        'shortName': shortName,
        'description': description,
        'category': category,
        'type': species,
        'genre': genre,
        'language': language,
        'size': size,
        'thumbnail': thumbnail,
        'images': images if images else None,
        'uploader': uploader,
        'uploaderLink': uploaderLink,
        'downloads': downloads,
        'lastChecked': lastChecked,
        'uploadDate': uploadDate,
        'seeders': seeders,
        'leechers': leechers,
        'magnetLink': magnetLink,
        'infoHash': infoHash.strip() if infoHash else None
    }

# screen clear code
def clear():
    # for windows
    if os.name == 'nt':
        os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        os.system('clear')

# Handle the streaming of the data
def handleStream(magnet_link, download):
    try:
        cmd = ""
        browser = False
        # print("Magnet Link: {}".format(magnet_link))
        cmd+="webtorrent \""
        cmd+=str(magnet_link)+"\""
        if not download:
            while True:
                choose = int(input(termcolor.colored("\nChoose your player\n\t0. Browser (file download & stream)\n\t1. Apple TV\n\t2. Chromecast\n\t3. Mplayer\n\t4. MPV\n\t5. OMX[HDMI]\n\t6. VLC\n\t7. XBMC\nChoice: ","green")))
                if choose == 0:
                    browser = True
                    break
                elif choose == 1:
                    cmd+=" --airplay"
                    break
                elif choose == 2:
                    cmd+=" --chromecast"
                    break
                elif choose == 3:
                    cmd+=" --mplayer"
                    break
                elif choose == 4:
                    cmd+=" --mpv"
                    break
                elif choose == 5:
                    cmd+=" --omx"
                    break
                elif choose == 6:
                    cmd+=" --vlc"
                    break
                elif choose == 7:
                    cmd+=" --xbmc"
                    break
                else:
                    print("\nInvalid input...\n")
        if browser:
            print("Click on the server link...")
        figgle = pyfiglet.Figlet(font="speed")
        print(termcolor.colored(figgle.renderText("Done!"),"green"))
        os.system(cmd)
    except Exception as e:
        print(e)
        print("\nSomething went wrong..")
        print("Please try again...\n")
        handleStream(magnet_link, download)

# Create link
def link(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)

clear() # clear the screen
print("Running the code...")

torrent = py1337x()

# category data
catdata = {
    1: 'movies',
    2: 'tv',
    3: 'games',
    4: 'music',
    5: 'apps',
    6: 'anime',
    7: 'documentaries',
    8: 'xxx',
    9: 'others',
}

# intro printing
def intro():
    figlet_format = pyfiglet.Figlet(font='speed')
    print(termcolor.colored(figlet_format.renderText('BinGer'), 'green'))
    # version printing
    print(termcolor.colored("Version: 2.0.0", 'green'))
    # Description of the program
    print("""BinGer is a program that allows you torrent without getting banned and without any hassle just click and enjoy. We have the following categories:\n
    1. 'movies'
    2. 'tv'
    3. 'games'
    4. 'music'
    5. 'apps'
    6. 'anime'
    7. 'documentaries'
    8. 'xxx'
    9. 'others'""")
    print("\n")

# the main code starts here
clear()
intro()

page = 1

# To get the category
while True:
    cat = int(input(termcolor.colored("\nEnter the category you want to browse: ","green")))
    if cat in catdata:
        break
    else:
        print("\nInvalid input...\n")

search_token = input(termcolor.colored("Enter the {} search token: ".format(catdata[cat]),"blue"))
more = 'y'
resultDict = {}
# result = []
sr = 1
magnet = []
try:
    clear()
    intro()
    while more == 'y' or more == 'Y':
        resultDict = torrent.search(search_token, category = catdata[cat], sortBy='seeders', page=page)
        # result.append(resultDict['items'])
        page+=1
        if len(resultDict['items'])>0:
            with open('bingerResults', 'a') as f:
                json.dump(resultDict, f)
            
            print(termcolor.colored("Search results for {}:".format(search_token),"green"))

            # display the results
            for item in resultDict['items']:
                magnet.append((torrent.info(torrentId=item['torrentId']))['magnetLink'])
                # print((torrent.info(torrentId=item['torrentId']))['magnetLink'])
                print(termcolor.colored("{}. ".format(sr),'green'),end="")
                print(termcolor.colored("{}".format(link(item['link'],label=item['name'])),'blue'),end="")
                print(termcolor.colored("\t{}".format(item['size']),'green'))
                sr+=1
        else:
            print(termcolor.colored("\nNo results found...\n","red"))
        # check for the loop to break
        more = input(termcolor.colored("\nDo you want to see more results? (y/n): ","green"))
    
    # Asking for the number of the search to be streamed or downloaded
    while True:
        num = int(input(termcolor.colored("\nEnter the number of the search you want to stream/download: ","blue")))-1
        if num in range(sr):
            break
        else:
            print("\nInvalid input...\n")

    download = False
    # Asking for a choice of downlaod or stream
    while True:
        choice = int(input(termcolor.colored("\nChoose your option:\n\t1. Download\n\t2. Stream\nChoice: ","yellow")))
        if choice == 1:
            download = True
            break
        elif choice == 2:
            download = False
            break
        else:
            print("\nInvalid input...\n")
    
    handleStream(magnet_link=magnet[num], download=download)


except Exception as e:
    print(e)
    print(termcolor.colored("\nSomething went wrong...","yellow"))
    print(termcolor.colored("Please try again...","red"))
    print(termcolor.colored("Exiting the program...\n","red"))