#!/usr/bin/env python3
# Cree ViridianCity_WestLane (couloir boise, memes tilesets que Jadielle) entre Jadielle et la Route 22 : NON re-executable.
import json,struct,os,shutil
W,H=16,14
ROAD_Y=6                      # rows 6,7 = route (Jadielle y 26,27)
os.makedirs('data/layouts/ViridianCityWestLane',exist_ok=True)
shutil.copy('data/layouts/ViridianCity/border.bin','data/layouts/ViridianCityWestLane/border.bin')
g=[]
for y in range(H):
    for x in range(W):
        if y==ROAD_Y: v=0x328d
        elif y==ROAD_Y+1: v=0x328e
        else:
            base=0x1d4 if y%2==0 else 0x1dc
            v=0x400|(base+(x%2))     # collision 1, elevation 0 (comme les arbres de Jadielle: 0x05d4)
        g.append(v)
open('data/layouts/ViridianCityWestLane/map.bin','wb').write(struct.pack('<%dH'%len(g),*g))
L=json.load(open('data/layouts/layouts.json'))
L['layouts'].append({"id":"LAYOUT_VIRIDIAN_CITY_WEST_LANE","name":"ViridianCityWestLane_Layout","width":W,"height":H,"border_width":2,"border_height":2,
 "primary_tileset":"gTileset_GeneralOpal","secondary_tileset":"gTileset_RustboroOpal",
 "border_filepath":"data/layouts/ViridianCityWestLane/border.bin","blockdata_filepath":"data/layouts/ViridianCityWestLane/map.bin"})
json.dump(L,open('data/layouts/layouts.json','w'),indent=2); open('data/layouts/layouts.json','a').write('\n')
os.makedirs('data/maps/ViridianCity_WestLane',exist_ok=True)
m={"id":"MAP_VIRIDIAN_CITY_WEST_LANE","name":"ViridianCity_WestLane","layout":"LAYOUT_VIRIDIAN_CITY_WEST_LANE","music":"MUS_PEWTER",
 "region_map_section":"MAPSEC_VIRIDIAN_CITY","requires_flash":False,"weather":"WEATHER_SUNNY","map_type":"MAP_TYPE_TOWN",
 "allow_cycling":True,"allow_escaping":False,"allow_running":True,"show_map_name":False,"floor_number":0,"battle_scene":"MAP_BATTLE_SCENE_NORMAL",
 "connections":[{"map":"MAP_VIRIDIAN_CITY","offset":-20,"direction":"right"},{"map":"MAP_ROUTE22","offset":-1,"direction":"left"}],
 "object_events":[],"warp_events":[],"coord_events":[],"bg_events":[]}
json.dump(m,open('data/maps/ViridianCity_WestLane/map.json','w'),indent=2); open('data/maps/ViridianCity_WestLane/map.json','a').write('\n')
open('data/maps/ViridianCity_WestLane/scripts.inc','w').write('ViridianCity_WestLane_MapScripts::\n\t.byte 0\n')
# V and Route22 connections
for name,old,new in (('ViridianCity','MAP_ROUTE22','MAP_VIRIDIAN_CITY_WEST_LANE'),('Route22','MAP_VIRIDIAN_CITY','MAP_VIRIDIAN_CITY_WEST_LANE')):
    p='data/maps/%s/map.json'%name; d=json.load(open(p))
    for c in d['connections']:
        if c['map']==old:
            c['map']=new
            c['offset']=20 if name=='ViridianCity' else 1
    json.dump(d,open(p,'w'),indent=2); open(p,'a').write('\n')
G=json.load(open('data/maps/map_groups.json'))
G['gMapGroup_TownsAndRoutes'].append('ViridianCity_WestLane')
i=G['connections_include_order'].index('ViridianCity'); G['connections_include_order'].insert(i+1,'ViridianCity_WestLane')
json.dump(G,open('data/maps/map_groups.json','w'),indent=2); open('data/maps/map_groups.json','a').write('\n')
s=open('data/event_scripts.s').read()
s=s.replace('\t.include "data/maps/Route22/scripts.inc"\n','\t.include "data/maps/Route22/scripts.inc"\n\t.include "data/maps/ViridianCity_WestLane/scripts.inc"\n',1)
open('data/event_scripts.s','w').write(s)
h=open('include/topaze_fog_pairs.h').read()
h=h.replace('{LAYOUT_VIRIDIAN_CITY, LAYOUT_ROUTE22}','{LAYOUT_VIRIDIAN_CITY_WEST_LANE, LAYOUT_ROUTE22}').replace('{LAYOUT_ROUTE22, LAYOUT_VIRIDIAN_CITY}','{LAYOUT_ROUTE22, LAYOUT_VIRIDIAN_CITY_WEST_LANE}')
open('include/topaze_fog_pairs.h','w').write(h)
