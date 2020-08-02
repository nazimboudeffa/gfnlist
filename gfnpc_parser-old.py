import wget
import json
import os
import sys

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
                    if game['publisher'] == 'Electronic Arts Inc.' :
                        sl = 'Origin'
                    if game['publisher'] == 'Ubisoft' :
                        sl = 'Uplay'
                    if game['publisher'] == 'Epic Games, Inc.' :
                        sl = 'Epic Games Launcher'
                    if game['publisher'] == 'Deep Silver' :
                        sl = 'Epic Games Launcher'
                    if game['publisher'] == 'YAGER Development' :
                        sl = 'Epic Games Launcher'
                    if game['publisher'] == 'NCSOFT' :
                        sl = 'NCSOFT Launcher'
                    if game['publisher'] == 'Riot Games' :
                        sl = 'LoL Launcher'
                    if game['publisher'] == 'Wargaming' :
                        sl = 'Wargaming Launcher'
                    if game['publisher'] == 'Bethesda Softworks' :
                        sl = 'Bethesda Launcher'
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
parse()
