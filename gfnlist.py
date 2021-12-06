import wget
import json
import os
import sys

header = "\
  ___________________                           _______                  \n\
 /  _____/\_   _____/__________   ____  ____    \      \   ______  _  __ \n\
/   \  ___ |    __)/  _ \_  __ \_/ ___\/ __ \   /   |   \ /  _ \ \/ \/ / \n\
\    \_\  \|     \(  <_> )  | \/\  \__\  ___/  /    |    (  <_> )     /  \n\
 \______  /\___  / \____/|__|    \___  >___  > \____|__  /\____/ \/\_/   \n\
        \/     \/                    \/    \/          \/                \n"

def main():

    menu()

def menu():

    print (header)
    print ("version 0.1")

    choice = input("""
                      A: Generate DATA.JSON
                      B: Generate CHANGELOG
                      C: Generate STEAMLIST.JSON
                      Q: Quit/Log Out
                      Please enter your choice: """)

    if choice == "A" or choice =="a":
        parse()
    elif choice == "B" or choice =="b":
        changelog()
    elif choice == "C" or choice =="c":
        steamlist()
    elif choice=="Q" or choice=="q":
        sys.exit
    else:
        print("You must only select either A, B or Q.")
        print("Please try again")
        menu()

def changelog():

    filepath = 'changelog.txt'

    if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...")
       sys.exit()

    with open(filepath, encoding="utf8") as fp:
       data = []
       for line in fp:
           print('<li><span class="badge badge-success">Added</span> ' + line.strip('\n') + '</li>')
def steamlist():
    with open('gfnpc.json', encoding="utf8") as f :
            games = json.loads(f.read())
            data = {}
            data['data'] = []
            for game in games :
                if game['steamUrl'] != '' :
                    sl = game['steamUrl']
                    data['data'].append({
                        'title': game['title'],
                        'id': sl.replace('https://store.steampowered.com/app/','')
                    })
            with open('public/steamlist.json', 'w') as outfile:
                json.dump(data, outfile)
def parse() :
    if not os.path.exists('gfnpc.json') :
        fs = wget.download(url='https://static.nvidiagrid.net/supported-public-game-list/locales/gfnpc-en-GB.json', out='gfnpc.json')
        with open('gfnpc.json', encoding="utf8") as f :
            games = json.loads(f.read())
    else :
        with open('gfnpc.json', encoding="utf8") as f :
            games = json.loads(f.read())
            data = {}
            data['data'] = []
            for game in games :
                #hs = 'No'
                fo = 'No'
                ftp = 'No'
                sl = 'N/A'
                g = ','.join(game['genres'])
                #if game['isHighlightsSupported'] :
                #    hs = 'Yes'
                if game['status'] == 'AVAILABLE' :
                    ac = 'Yes'
                if game['isFullyOptimized'] :
                    fo = 'Yes'
                for genre in game['genres'] :
                    if genre == 'Free To Play' :
                        ftp = 'Yes'
                if game['steamUrl'] == '' :
                    if game['store'] == '' :
                        sl = 'N/A'
                        """ TODO : Get the name of the launchers
                        if game['publisher'] == 'Electronic Arts Inc.' :
                            sl = 'Origin'
                        if game['publisher'] == 'NCSOFT' :
                            sl = 'NCSOFT'
                        if game['publisher'] == 'Riot Games' :
                            sl = 'LoL Launcher'
                        if game['publisher'] == 'Gaijin Entertainment' :
                            sl = 'Wargaming'
                        """
                    else :
                        sl = game['store']
                else :
                    sl = 'Steam'
                data['data'].append({
                    'title': game['title'],
                    'publisher': game['publisher'],
                    'genre': g,
                    #'hs': hs,
                    'fo': fo,
                    'ftp': ftp,
                    'sl': sl,
                    'ac': ac
                })
            with open('public/data.json', 'w') as outfile:
                json.dump(data, outfile)

if __name__ == '__main__':
    main()
