"""
Created on Tue Sep  4 20:49:07 2018

@author: martrepodi
"""

import requests
from json import loads, dumps

class api_swgoh_help():
    def __init__(self, settings):
        self.user = "username=" + settings.username
        self.user += "&password=" + settings.password
        self.user += "&grant_type=password"
        self.user += "&client_id=" + settings.client_id
        self.user += "&client_secret=" + settings.client_secret

        self.token = {}
        self.logged_in = False

        self.urlBase = 'https://api.swgoh.help'
        self.signin = '/auth/signin'
        self.endpoints = {'guilds': '/swgoh/guilds',
                          'players': '/swgoh/players',
                          'rosters': '/swgoh/rosters',
                          'data': '/swgoh/data',
                          'units': '/swgoh/units',
                          'zetas': '/swgoh/zetas',
                          'squads': '/swgoh/squads',
                          'events': '/swgoh/events',
                          'battles': '/swgoh/battles'}

        if settings.statsUrl:
            self.statsUrl = settings.statsUrl
        else:
            self.statsUrl = 'https://crinolo-swgoh.glitch.me/baseStats/api/'

        if settings.charStatsApi:
            self.charStatsApi = settings.charStatsApi
        else:
            self.charStatsApi = 'https://crinolo-swgoh.glitch.me/statCalc/api/characters'

        if settings.shipStatsApi:
            self.shipStatsApi = settings.shipStatsApi
        else:
            self.shipStatsApi = 'https://crinolo-swgoh.glitch.me/statCalc/api/ships'

        self.verbose = settings.verbose if settings.verbose else False
        self.debug = settings.debug if settings.debug else False
        self.dump = settings.dump if settings.dump else False

        self.data_type = {'guild':'/swgoh/guild/',
                          'player':'/swgoh/player/',
                          'data':'/swgoh/data/',
                          'units':'/swgoh/units',
                          'battles':'/swgoh/battles'}
        
    def get_token(self):
        sign_url = self.urlBase+self.signin
        payload = self.user
        head = {"Content-type": "application/x-www-form-urlencoded",
                'Content-Length': str(len(payload))}
        r = requests.request('POST',sign_url, headers=head, data=payload, timeout = 10)
        if r.status_code != 200:
            error = 'Cannot login with these credentials'
            return  {"status_code" : r.status_code,
                     "message": error}
        _tok = loads(r.content.decode('utf-8'))['access_token']
        self.token = { 'Authorization':"Bearer "+_tok} 
        return(self.token)

    def fetchAPI(self, url, payload):
        self.get_token()
        head = {'Content-Type': 'application/json', 'Authorization': self.token['Authorization']}
        data_url = self.urlBase + url
        try:
            r = requests.request('POST', data_url, headers=head, data=dumps(payload))
            if r.status_code != 200:
                print("Error posting data...")
                error = 'Cannot fetch data - error code'
                data = {"status_code": r.status_code,
                        "message": error}
            else:
                data = loads(r.content.decode('utf-8'))
        except Exception as e:
            data = {"message": 'Cannot fetch data'}
        return data

    def fetchZetas(self):
        try:
            return self.fetchAPI(self.endpoints['zetas'], {})
        except Exception as e:
            return str(e)

    def fetchSquads(self):
        try:
            return self.fetchAPI(self.endpoints['squads'], {})
        except Exception as e:
            return str(e)

    def fetchBattles(self, payload):
        try:
            return self.fetchAPI(self.endpoints['battles'], payload)
        except Exception as e:
            return str(e)

    def fetchEvents(self, payload):
        if not payload:
            payload = { "language": "eng_us", "enums": True }
        try:
            return self.fetchAPI(self.endpoints['events'], payload)
        except Exception as e:
            return str(e)

    def fetchData(self, payload):
        try:
            return self.fetchAPI(self.endpoints['data'], payload)
        except Exception as e:
            return str(e)

    def fetchPlayers(self, payload):
        try:
            return self.fetchAPI(self.endpoints['players'], payload)
        except Exception as e:
            return str(e)

    def fetchGuild(self, payload):
        try:
            return self.fetchAPI(self.endpoints['guilds'], payload)
        except Exception as e:
            return str(e)

    def fetchUnits(self, payload):
        try:
            return self.fetchAPI(self.endpoints['units'], payload)
        except Exception as e:
            return str(e)

    def fetchRoster(self, payload):
        try:
            return self.fetchAPI(self.endpoints['roster'], payload)
        except Exception as e:
            return str(e)

    def rosterStats(self, unit, flags, type):
        try:
            if not unit:
                raise ValueError('No units passed to stats calc!')
            if type(unit) is not list:
                unit = [unit]
            payload = []
            for u in unit:
                payload.push({'defId': u.defId,
                              'rarity': u.rarity,
                              'level': u.level,
                              'gear': u.gear,
                              'equipped': u.equipped,
                              'mods': u.mods
                              })
            apiUrl = self.shipStatsApi if type and (type == 'SHIP' or type == 2) else self.charStatsApi
            apiUrl += '?flags=' + flags if flags else ''

            data = dumps(payload)
            head = {'Content-Type': 'application/json'}
            r = requests.request('POST', apiUrl, headers=head, data=data)
            if r.status_code != 200:
                error = 'Cannot fetch data - error code'
                data = {"status_code": r.status_code,
                        "message": error}
            else:
                data = loads(r.content.decode('utf-8'))
            return data
        except Exception as e:
            return str(e)

    def unitStats(self, unit, flags, type):
        try:
            if not unit:
                raise ValueError('No units passed to stats calc!')

            apiUrl = self.shipStatsApi if type and (type == 'SHIP' or type == 2) else self.charStatsApi
            apiUrl += '?flags=' + flags if flags else ''

            data = dumps(unit)
            head = {'Method': 'POST', 'Content-Type': 'application/json'}
            r = requests.request('POST', apiUrl, headers=head, data=data)
            if r.status_code != 200:
                error = 'Cannot fetch data - error code'
                data = {"status_code": r.status_code,
                        "message": error}
            else:
                data = loads(r.content.decode('utf-8'))
            return data
        except Exception as e:
            return str(e)

    def calcStats(self, allycode, *args, **kwargs):
        print("Entering calcStats...")
        if not allycode:
            raise ValueError('No allycode passed to stats calc!')

        baseId = kwargs.get('baseId', '')
        baseId = baseId.upper()
        print("BaseId: " + baseId)
        type = kwargs.get('type', '')
        print("Type: " + type)
        flags = kwargs.get('flags', [])
        flags = ','.join(str(x) for x in flags)
        print("Flags: " + flags)

        apiUrl = self.shipStatsApi if (type and (type == 'SHIP' or type == 2)) else self.charStatsApi
        apiUrl += '/player/' + str(allycode)
        apiUrl += '/' + baseId if baseId else ''
        apiUrl += '?flags=' + flags if flags else ''

        head = {'Content-Type': 'application/json'}
        print("URL: " + apiUrl)
        r = requests.request('GET', apiUrl, headers=head)
        if r.status_code != 200:
            error = 'Cannot fetch data - error code'
            data = {"status_code": r.status_code,
                    "message": error}
        else:
            data = loads(r.content.decode('utf-8'))

        return (data)

    def fetchStats(self, allycode, *args, **kwargs):
        apiUrl = self.charStatsApi + '/player/' + str(allycode) + '?flags=withModCalc,gameStyle'
        head = {'Content-Type': 'application/json'}
        print("URL: " + apiUrl)
        r = requests.request('GET', apiUrl, headers=head)
        if r.status_code != 200:
            error = 'Cannot fetch data - error code'
            data = {"status_code": r.status_code,
                    "message": error}
        else:
            data = loads(r.content.decode('utf-8'))

        return (data)

class settings():
    def __init__(self, _username, _password, *args, **kwargs):
        self.username = _username
        self.password = _password
        self.client_id = kwargs.get('client_id', '123')
        self.client_secret = kwargs.get('client_secret', 'abc')
        self.statsUrl = kwargs.get('statsUrl', '')
        self.charStatsApi = kwargs.get('charStatsApi', '')
        self.shipStatsApi = kwargs.get('shipStatsApi', '')
        self.verbose = kwargs.get('verbose', False)
        self.debug = kwargs.get('debug', False)
        self.dump = kwargs.get('dump', False)
