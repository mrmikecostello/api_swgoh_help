#!/usr/bin/env python3

import json

from api_swgoh_help import api_swgoh_help, settings

# Initialize data structures
toons = {}
skills = {}
abilities = {}
gear = {}

creds = settings('MarTrepodi', 'yGv-y74-eUu-cNn')
client = api_swgoh_help(creds)

allycodes = [314927874]

client.get_token()

# Build local units list
payload = {}
payload['collection'] = "unitsList"
payload['language'] = "eng_us"
payload['enums'] = True
payload['match'] = {"rarity": 7,
                    "obtainable": True,
                    "obtainableTime": 0
                    }
payload['project'] = {"baseId": 1,
                      "nameKey": 1,
                      "descKey": 1,
                      "forceAlignment": 1,
                      "categoryIdList": 1,
                      "combatType": 1
                      }
units = client.fetchData(payload)

for unit in units:
    toons[unit['baseId']] = unit

# Build local skills list
payload = {}
payload['collection'] = "skillList"
payload['language'] = "eng_us"
payload['enums'] = True
payload['project'] = { "id": 1,
                       "abilityReference": 1,
                       "isZeta": 1
                       }
items = client.fetchData(payload)

for skill in items:
    skills[skill['id']] = skill

# Build local abilities list
# skills[id]['abilityReference'] -> abilities[id]
payload = {}
payload['collection'] = "abilityList"
payload['language'] = "eng_us"
payload['enums'] = True
payload['project'] = { "id": 1,
                       "type": 1,
                       "nameKey": 1
                       }
items = client.fetchData(payload)
for ability in items:
    abilities[ability['id']] = ability['nameKey']

# Build local gear list
payload = {}
payload['collection'] = "equipmentList"
payload['language'] = "eng_us"
payload['enums'] = True
payload['project'] = {"id": 1,
                      "nameKey": 1
                      }
items = client.fetchData(payload)
for item in items:
    gear[item['id']] = item['nameKey']

payload = {}
payload['allycodes'] = allycodes
payload['language'] = "eng_us"
payload['enums'] = True
# Remove the project payload element to retrieve the player's entire roster
payload['project'] = { "name": 1 }

#print("Players\n-------")
#players = client.fetchPlayers(payload)
#print(json.dumps(players, indent=2))

# mods = client.fetchPlayers(allycode)
# zetas = client.fetchZetas()
# stats = client.calcStats(allycode)

# print("\nMods\n-------")
# print(json.dumps(mods, indent=2))
# print("\nZetas\n-------")
# print(json.dumps(zetas, indent=2))

