import requests
import xmltodict
import secrets
import variables
import sys
import urllib
import datetime


class API():
    def __init__(self, options):
        if('--debug' in options):
            self.debug = True
        else:
            self.debug = False

        self.ip_address = '192.168.21.1'  # set this to your own LAN IP
        self.device_address = 'http://%s/mml.do' % self.ip_address
        self.email = secrets.vars['email']
        self.username = secrets.vars['user']
        self.ssid = secrets.vars['ssid']
        self.password = secrets.vars['password']
        self.api_key = secrets.vars['api_key']
        self.zipcode = secrets.vars['zipcode']
        self.tuneable_frequencies = variables.tuneable_frequencies
        self.scanable_frequencies = variables.scanable_frequencies
        self.connect()

        if(len(sys.argv) > 1 and sys.argv[1] != '--debug'):
            getattr(self, '%s' % sys.argv[1])()

    def sendCMD(self, PARAMS):
        response = requests.get(self.device_address, params=PARAMS)
        if(self.debug):
            print("Request made: %s?%s" %
                  (self.device_address, urllib.parse.urlencode(PARAMS)))
            print("Response from request: \n%s" % response.text)
            print("End of Response")

        try:
            return xmltodict.parse(response.text)
        except:
            print("Response is not xml format")
            return response

    def connect(self):
        params = {
            'cmd': 'connect',
            'clientid': 'Automated',
            'force': '1',
            'timeout': '86400',
            'clientUserId': self.email,
            'clientUserProfile': self.username
        }
        self.sessionid = self.sendCMD(params)['MML']['Body']['SessionID']
        print("Device connected with session id: %s" % self.sessionid)

    def disconnect(self):
        para = {
            'cmd': 'disconnect',
            'sessionid': self.sessionid
        }
        self.sendCMD(para)

    def getHomeNetworks(self):
        para = {
            'cmd': 'gethomenetworks',
            'sessionid': self.sessionid
        }
        self.wifi = self.sendCMD(para)

    def setWiFiNetwork(self):
        params = {
            'cmd': 'addnetwork',
            'sessionid': self.sessionid,
            'networkid': self.ssid,
            'user': self.username,
            'password': self.password,
            'priority': '0'
        }
        self.wifi = self.sendCMD(params)

    def getStorageStatus(self):
        para = {
            'cmd': 'getmediapaths',
            'sessionid': self.sessionid
        }
        self.storage = self.sendCMD(
            para)['MML']['Body']['Devices']['MediaDevice']

    def getPVRFileList(self):
        para = {
            'cmd': 'getpvrfilelist',
            'sessionid': self.sessionid
        }
        self.pvr = self.sendCMD(para)['MML']['Body']['PVRFiles']['PVRFile']

    def getSignalStatus(self):
        para = {
            'cmd': 'getstatusall',
            'sessionid': self.sessionid
        }
        self.status = self.sendCMD(para)['MML']['Body']['SignalStatistics']

    def reboot(self):
        para = {
            'cmd': 'reboot',
            'sessionid': self.sessionid
        }
        self.status = self.sendCMD(para)

    def getINAmode(self):
        para = {
            'cmd': 'getInamode',
            'sessionid': self.sessionid
        }
        self.mode = self.sendCMD(para)
        print(self.mode)

    def setINAmode(self):
        params = {
            'cmd': 'setInamode',
            'sessionid': self.sessionid,
            'mode': '1'
        }
        self.mode = self.sendCMD(params)

    def getDeviceInfo(self):
        para = {
            'cmd': 'getdeviceinfo',
            'sessionid': self.sessionid
        }
        self.device_info = self.sendCMD(para)['MML']['Body']['DeviceInfo']
        print(self.device_info)

    def getServiceInformationLists(self, uniqueid=None):
        uniqueid = '53300301'
        para = {
            'cmd': 'getserviceinformationlists',
            'sessionid': self.sessionid,
            'uniqueid': "%s" % uniqueid
        }
        self.service = self.sendCMD(para)
        print(self.service)

    def startRecording(self, filename, recording_length):
        para = {
            'cmd': 'startrecording',
            'sessionid': self.sessionid,
            'mediapath': 'data',
            'duration': '%s' % str(recording_length),
            'fileprefix': '%s' % str(filename)
        }  # Needs work
        self.record = self.sendCMD(para)

    def stopRecording(self):
        para = {
            'cmd': 'stoprecording',
            'sessionid': self.sessionid
        }
        self.record = self.sendCMD(para)

    def startScan(self):
        para = {
            'cmd': 'startscan',
            'sessionid': self.sessionid,
            'force': '1',
            'freqbwlist': self.scanable_frequencies,
            'location': 'Location1'
        }
        self.scan = self.sendCMD(para)

    def getScanStatus(self):
        para = {
            'cmd': 'getscanstatus',
            'sessionid': self.sessionid
        }
        self.scan = self.sendCMD(para)['MML']['Body']['ScanStatus']
        print(self.scan)

    def stopScan(self):
        params = {
            'cmd': 'stopscan',
            'sessionid': self.sessionid,
            'discardservicesfound': '0',
            'eraseservicelist': '1'
        }
        self.scan = self.sendCMD(params)

    def downloadFirmware(self, filename=None):
        # need a way of getting this filename
        filename = 'WatchAir_sw_v1.9.1_1521007676.zip'
        response = requests.get('http://cf.watchairtv.com/sys/%s' % filename)
        with open(filename, 'wb') as file:
            file.write(response.content)
        
        self.firmware = xmltodict.parse(response.text)

    def upgradeFirmwarePrepare(self):
        para = {
            'cmd': 'upgradefirmwareprepare',
            'sessionid': self.sessionid
        }
        self.firmware = self.sendCMD(para)

    def pushFile(self):
        params = {
            'cmd': 'pushfile',
            'sessionid': self.sessionid,
            'force': '1',
            'fullpath': 'data/firmware.zip'
        }
        self.firmware = self.sendCMD(params)

    # needs work to be dynamic
    def streamVideo(self, uniqueid=None, frequency=None, channel_ts_id=None):
        uniqueid = '53300305'
        frequency = self.tuneable_frequencies['2']
        params = {
            'cmd': 'startstreamingdata',
            'sessionid': self.sessionid,
            'uniqueid': '%s' % str(uniqueid),
            'freq': '%s' % str(frequency)
        }
        self.video_stream = self.sendCMD(params)

    def getArtwork(self, asset_id):
        # id comes from api lineup grid call -> response['airings']['preferredImage']['uri'].split('/')[1]
        asset_id = 'p10005060_st_h13_ac.jpg'
        url = 'http://epic.tmsimg.com/assets/%s.jpg' % asset_id
        PARAMS = {
            'w': '240',
            'h': '135'
        }
        response = requests.get(url, params=PARAMS)
        with open('%s.jpg' % asset_id, 'wb') as file:
            file.write(response.content)

    def getLineups(self):
        # http://data.tmsapi.com/v1.1/lineups?country=USA&postalCode=27713&api_key=1234567890
        url = 'http://data.tmsapi.com/v1.1/lineups'
        PARAMS = {
            'country': 'USA',
            'postalCode': self.zipcode,
            'api_key': self.api_key
        }
        response = requests.get(url, params=PARAMS)
        if(self.debug):
            print("Request made: %s?%s" %
                  (url, urllib.parse.urlencode(PARAMS)))
            print("Response from request: \n%s" % response.text)
            print("End of Response")

        return xmltodict.parse(response.text)

    def getLineupGrid(self):
        # NCxxxxx is obtained by lineupId
        # http://data.tmsapi.com/v1.1/lineups/USA-NC32461-X/grid?startDateTime=2012-02-20T14:00Z&api_key=1234567890
        url = 'http://data.tmsapi.com/v1.1/lineups/USA-OTA%s-X/grid' % self.zipcode
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_hour = datetime.datetime.now().strftime("%H")
        PARAMS = {
            # 'country': 'USA',
            # 'postalCode': self.zipcode,
            # 'stationId': '66570',  # don't know what these values mean, and probably need work
            'startDateTime': '%sT%s:00Z' % (current_date, current_hour),
            # 'endDateTime': '%sT%s-00Z' % (current_date, str(int(current_hour) + 1)),
            # 'imageSize': 'Sm',
            # 'imageAspectTV': '16x9',
            'api_key': self.api_key
        }
        response = requests.get(url, params=PARAMS)
        if(self.debug):
            print("Request made: %s?%s" %
                  (url, urllib.parse.urlencode(PARAMS)))
            print("Response from request: \n%s" % response.text)
            print("End of Response")

        return xmltodict.parse(response.text)

    def getLineupChannels(self):
        # http://data.tmsapi.com/v1.1/lineups/USA-NY55899-X/channels?api_key=1234567890
        url = 'http://data.tmsapi.com/v1.1/lineups/USA-OTA%s-X/channels' % self.zipcode
        PARAMS = {
            'api_key': self.api_key
        }
        response = requests.get(url, params=PARAMS)
        if(self.debug):
            print("Request made: %s?%s" %
                  (url, urllib.parse.urlencode(PARAMS)))
            print("Response from request: \n%s" % response.text)
            print("End of Response")

        return xmltodict.parse(response.text)

    def newShowListings(self, zipcode=None):
        url = 'http://data.tmsapi.com/v1.1/programs/newShowAirings'
        PARAMS = {
            'lineupId': 'USA-OTA%s' % self.zipcode,
            'startDateTime': "%s" % datetime.datetime.now().strftime("%Y-%m-%dT%H:00Z"),
            'api_key': self.api_key
        }
        response = requests.get(url, params=PARAMS)
        if(self.debug):
            print("Request made: %s?%s" %
                  (url, urllib.parse.urlencode(PARAMS)))
            if(len(response.text) > 100):
                with open('response.json', 'wb') as file:
                    file.write(response.content)
            else:
                print("Response from request: \n%s" % response.text)
            print("End of Response")

        return response.text


if __name__ == "__main__":
    WA_Antenna = API(sys.argv)
