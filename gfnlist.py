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
                      Q: Quit/Log Out
                      Please enter your choice: """)

    if choice == "A" or choice =="a":
        parse()
    elif choice == "B" or choice =="b":
        changelog()
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

def parse() :
    if not os.path.exists('gfnpc.json') :
        fs = wget.download(url='https://static.nvidiagrid.net/supported-public-game-list/gfnpc.json', out='gfnpc.json')
        with open('gfnpc.json', encoding="utf8") as f :
            games = json.loads(f.read())
    else :
        with open('gfnpc.json', encoding="utf8") as f :
            games = json.loads(f.read())
            data = {}
            data['data'] = []
            for game in games :
                hs = 'No'
                fo = 'No'
                ftp = 'No'
                sl = 'Steam'
                g = ','.join(game['genres'])
                #if game['isHighlightsSupported'] :
                #    hs = 'Yes'
                if game['isFullyOptimized'] :
                    fo = 'Yes'
                for genre in game['genres'] :
                    if genre == 'Free To Play' :
                        ftp = 'Yes'
                if game['steamUrl'] == '' :
                    if game['store'] == 'Origin' :
                        sl = 'Origin'
                    if game['store'] == 'UPLAY' :
                        if 'russia' in game['sortName'] : sl = 'Uplay Russia'
                        else : sl = 'Uplay'    
                    if game['store'] == 'Epic' :
                        sl = 'Epic Games Launcher'
                    if game['publisher'] == 'NCsoft Corp.' :
                        sl = 'NCSOFT Launcher'
                    if game['publisher'] == 'Riot Games, Inc.' :
                        sl = 'LoL Launcher'
                    if game['publisher'] == 'Wargaming Group Limited' :
                        if 'asia' in game['sortName'] : sl = 'Wargaming Asia'
                        if 'europe' in game['sortName'] : sl = 'Wargaming Europe'
                        if 'north_america' in game['sortName'] : sl = 'Wargaming North America'
                        if 'russia' in game['sortName'] : sl = 'Wargaming Russia'
                    if game['publisher'] == 'Bethesda Softworks' :
                        sl = 'Bethesda Launcher'
                    if game['publisher'] == 'Gaijin Entertainment' :
                        sl = 'WARTHUNDER'
                    if game['publisher'] == 'DMM Games' :
                        sl = 'WARTHUNDER Japan'
                data['data'].append({
                    'title': game['title'],
                    'publisher': game['publisher'],
                    'genre': g,
                    #'hs': hs,
                    'fo': fo,
                    'ftp': ftp,
                    'sl': sl
                })
            with open('public/data.json', 'w') as outfile:
                json.dump(data, outfile)

if __name__ == '__main__':
    main()
