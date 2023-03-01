import os
from os import system, name
import json

def clear():
    try:
        config = json.load(fp=open('config.json'))
        if config["py1337x"]!=True:
            system("pip install 1337x")
            system("pip install py1337x")
            config["py1337x"]=True
        elif config["pyfiglet"]!=True:
            system("pip install pyfiglet")
            config["pyfiglet"]=True
        elif config["termcolor"]!=True:
            system("pip install termcolor")
            config["termcolor"]=True
        elif config["webtorrent"]!=True:
            system("pip install webtorrent")
            config["webtorrent"]=True
        json.dump(config, fp=open('config.json', 'w'))
    except Exception as e:
        print(e)
        os.system("pip install pyfiglet")
        os.system("pip install termcolor")
        os.system("pip install 1337x")
        os.system("pip install py1337x")
        os.system("npm install -g webtorrent")
        config = {
            "py1337x": True,
            "pyfiglet": True,
            "termcolor": True,
            "webtorrent": True,
        }
    
    with open('config.json', 'w') as f:
        json.dump(config, f)
    
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')


# library check and install
clear()
print("Checking for updates...")
from py1337x import py1337x
import pyfiglet
import termcolor
print("Runnning the file...")

torrent = py1337x()

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

def handleStream(magnet_link, download):
    try:
        cmd = ""
        # print("Magnet Link: {}".format(magnet_link))
        cmd+="webtorrent \""
        cmd+=str(magnet_link)+"\""
        if not download:
            while True:
                choose = int(input("\nChoose your player\n\t1. Apple TV\n\t2. Chromecast\n\t3. Mplayer\n\t4. MPV\n\t5. OMX[HDMI]\n\t6. VLC\n\t7. XBMC\nChoice: "))
                if choose == 1:
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
        os.system(cmd)
    except Exception as e:
        print(e)
        print("\nSomething went wrong...\n")
        print("\nPlease try again...\n")
        handleStream(magnet_link, download)
    
def intro():
    figlet_format = pyfiglet.Figlet(font='speed')
    print(termcolor.colored(figlet_format.renderText('BinGer'), 'green'))
    # version printing
    print(termcolor.colored("Version: 1.0.0", 'green'))
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


if __name__ == "__main__":
    # intro
    clear()
    intro()

    # To get the categories
    while True:
        cat = int(input(termcolor.colored("\nEnter the category you want to browse: ", 'green')))
        if cat in [1,2,3,4,5,6,7,8,9]:
            break
        else:
            print("\nInvalid input...\n")
    # To get the search token
    movie_name = input("Enter the {} name for searching: ".format(catdata[cat]))
    try:
        result = torrent.search(movie_name, category=catdata[cat], sortBy='seeders') 
        if len(result['items']) > 0:
            with open('result.json','w') as file:
                json.dump(result,file)
            magnet = []
            count = 1

            clear()
            intro()
            print(termcolor.colored("\nSearch results:", 'green'))

            # display the search results with size
            for movie in result['items']:
                magnet.append((torrent.info(torrentId=movie['torrentId']))['magnetLink'])
                print(termcolor.colored("{} -> ".format(count), 'green'), end="")
                print("{} : ".format(movie['name']), end="")
                print(termcolor.colored("{}".format(movie['size']), 'green'))
                count+=1
            
            while True:
                choice = (int(input("\nEnter a choice for downloading/streaming: ")))-1
                if choice in range(len(result['items'])):
                    break
                else:
                    print("\nInvalid input...\n")

            if cat in  [1,2,4,6,7,8]:
                download = False
                stream_choice = int(input("\nDo you want to stream the movie: \n\t 1-> Stream\n\t 2-> Download\nChoice: "))
                while True:
                    if stream_choice == 1:
                        # Streaming
                        download = False
                        handleStream(magnet_link=magnet[choice], download=download)
                        break
                    elif stream_choice == 2:
                        # Downloading
                        download = True
                        break
                    else:
                        print("\nWrong Choice enter again...\n")
            else:
                download = True
                handleStream(magnet_link=magnet[choice], download=download)
        else:
            print("\nNo results found...\n")
    except Exception as e:
        print(e)
        print("\nSomething went wrong...\n")
        print("\nTry again...\n")
        exit()