import wget
import json
import os
import sys
import requests
from privkey import key
import csv

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
                      D: Generate STEAM OFFERS
                      E: Generate ONE STEAM OFFER
                      F: Generate GFN STEAM CSV
                      Q: Quit/Log Out
                      Please enter your choice: """)

    if choice == "A" or choice =="a":
        parse()
    elif choice == "B" or choice =="b":
        changelog()
    elif choice == "C" or choice =="c":
        steamlist()
    elif choice == "D" or choice =="d":
        steamoffers()
    elif choice == "E" or choice =="e":
        steamoneoffer()
    elif choice == "F" or choice =="f":
        gfnsteamcsv()
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
def steamoffers():
    with open('public/steamlist.json', encoding="utf8") as f :
            d = json.loads(f.read())
            games = d['data']
            data = {}
            data['data'] = []
            for game in games :
                g = requests.get("http://store.steampowered.com/api/appdetails/?appids="+game['id']+"&key="+key)
                gamejson = g.json()
                print('CHECKING GAME ID :' + str(game['id'])) 
                if 'data' in gamejson[game['id']] : 
                    if 'price_overview' in gamejson[game['id']]['data'] :
                        print('Any chance to get a discount in price overview ...')
                        if gamejson[game['id']]['data']['price_overview']['discount_percent'] != 0 :
                            print(gamejson[game['id']]['data']['name'] + ':' + str(gamejson[game['id']]['data']['steam_appid']))
                            print(gamejson[game['id']]['data']['price_overview'])
                            data['data'].append({
                                'title': gamejson[game['id']]['data']['name'],
                                'id': gamejson[game['id']]['data']['steam_appid'],
                                'initial': gamejson[game['id']]['data']['price_overview']['initial'],
                                'final': gamejson[game['id']]['data']['price_overview']['final'],
                                'discount': gamejson[game['id']]['data']['price_overview']['discount_percent']
                            })
                            with open('public/steamoffers.json', 'w') as outfile:
                                json.dump(data, outfile)
def steamoneoffer():
    g = requests.get("http://store.steampowered.com/api/appdetails/?appids=1128000")
    gamejson = g.json()
    print(gamejson)
    if gamejson != 'null' : 
        if 'data' in gamejson['1128000'] : 
            if 'price_overview' in gamejson['1128000']['data'] :
                if gamejson['1128000']['data']['price_overview']['discount_percent'] != 0 :
                    print(gamejson['1128000']['data']['name'] + ':' + str(gamejson['1128000']['data']['steam_appid']))
                    print(gamejson['1128000']['data']['price_overview'])
    else :
        print('null')
def gfnsteamcsv():
    with open('public/steamlist-forcsv.json', encoding="utf8") as f :
            d = json.loads(f.read())
            games = d['data']
            header = ['id', 'name', 'age', 'free', 'recommendations', 'date']
            datascience = []
            total = len(games)
            count = 0 
            with open('gfnsteam-temp.csv', 'w', newline ='', encoding='utf8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)
                for game in games :
                    g = requests.get("http://store.steampowered.com/api/appdetails/?appids="+game['id']+"&key="+key)
                    gamejson = g.json()
                    if gamejson != 'null' : 
                        if 'data' in gamejson[game['id']] : 
                            if 'recommendations' in gamejson[game['id']]['data'] :
                                print(gamejson[game['id']]['data']['name'] + ':' + str(gamejson[game['id']]['data']['steam_appid']))
                                print(str(count) + ' / ' + str(total))
                                datascience = [
                                    gamejson[game['id']]['data']['steam_appid'],
                                    gamejson[game['id']]['data']['name'],
                                    gamejson[game['id']]['data']['required_age'],
                                    gamejson[game['id']]['data']['is_free'],
                                    gamejson[game['id']]['data']['recommendations']['total'],
                                    gamejson[game['id']]['data']['release_date']['date']
                                ]
                                writer.writerow(datascience)
                                count = count + 1
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
