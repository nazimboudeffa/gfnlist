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
                sl = 'N/A'
                g = ','.join(game['genres'])
                #if game['isHighlightsSupported'] :
                #    hs = 'Yes'
                if game['isFullyOptimized'] :
                    fo = 'Yes'
                for genre in game['genres'] :
                    if genre == 'Free To Play' :
                        ftp = 'Yes'
                if game['store'] != 'Steam' :
                    if game['store'] == 'Origin' :
                        sl = 'Origin'
                    if '_uplay' in game['sortName'] :
                        sl = 'Uplay'
                    if '_epic_game' in game['sortName'] :
                        sl = 'Epic Games'
                    if '_epic' in game['sortName'] :
                        sl = 'Epic Games'
                    if '_albion_launcher' in game['sortName'] :
                        sl = 'Albion Launcher'
                    if game['publisher'] == 'YAGER Development' :
                        sl = 'Epic Games'
                    if game['publisher'] == 'NCsoft Corp.' :
                        sl = 'NCSOFT'
                    if game['publisher'] == 'Riot Games' :
                        sl = 'LoL Launcher'
                    if game['publisher'] == 'Wargaming' :
                        sl = 'Wargaming'
                    if game['publisher'] == 'Bethesda Softworks' :
                        sl = 'Bethesda'
                    if game['publisher'] == 'DMM Games' :
                        sl = 'Wargaming'
                    if game['publisher'] == 'Gaijin Entertainment' :
                        sl = 'Gaijin'
                else :
                    sl = 'Steam'
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
