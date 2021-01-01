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

        self.ip_address = '192.168.1.115'  # set this to your own LAN IP
        self.device_address = 'http://%s/mml.do' % self.ip_address
        self.email = secrets.vars['email']
        self.user_name = secrets.vars['user']
        self.ssid = secrets.vars['ssid']
        self.password = secrets.vars['password']
        self.api_key = secrets.vars['api_key']
        self.zipcode = secrets.vars['zipcode']
        self.frequencies = variables.frequencies
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
            'clientUserProfile': self.user_name
        }
        self.sessionid = self.sendCMD(params)['MML']['Body']['SessionID']
        print("Device connected with session id: %s" % self.sessionid)

    def disconnect(self):
        para = {
            'cmd': 'disconnect',
            'sessionid': str(self.sessionid)
        }
        self.sendCMD(para)

    def getHomeNetworks(self):
        para = {
            'cmd': 'gethomenetworks',
            'sessionid': str(self.sessionid)
        }
        self.wifi = self.sendCMD(para)

    def setWiFiNetwork(self):
        params = {
            'cmd': 'addnetwork',
            'sessionid': str(self.sessionid),
            'networkid': self.SSID,
            'user': self.user_name,
            'password': self.password,
            'priority': '0'
        }
        self.wifi = self.sendCMD(params)

    def getStorageStatus(self):
        para = {
            'cmd': 'getmediapaths',
            'sessionid': str(self.sessionid)
        }
        self.storage = self.sendCMD(
            para)['MML']['Body']['Devices']['MediaDevice']

    def getPVRFileList(self):
        para = {
            'cmd': 'getpvrfilelist',
            'sessionid': str(self.sessionid)
        }
        self.pvr = self.sendCMD(para)['MML']['Body']['PVRFiles']['PVRFile']

    def getSignalStatus(self):
        para = {
            'cmd': 'getstatusall',
            'sessionid': str(self.sessionid)
        }
        self.status = self.sendCMD(para)['MML']['Body']['SignalStatistics']

    def getINAmode(self):
        para = {
            'cmd': 'getInamode',
            'sessionid': str(self.sessionid)
        }
        self.mode = self.sendCMD(para)
        print(self.status)

    def setINAmode(self):
        params = {
            'cmd': 'setInamode',
            'sessionid': str(self.sessionid),
            'mode': '1'
        }
        self.mode = self.sendCMD(params)

    def getDeviceInfo(self):
        para = {
            'cmd': 'getdeviceinfo',
            'sessionid': str(self.sessionid)
        }
        self.device_info = self.sendCMD(para)['MML']['Body']['DeviceInfo']
        print(self.device_info)

    def getServiceInformationLists(self):
        para = {
            'cmd': 'getserviceinformationlists',
            'sessionid': str(self.sessionid),
            'uniqueid': '53300301'
        }
        self.service = self.sendCMD(para)
        print(self.service)

    def startRecording(self, filename, recording_length):
        para = {
            'cmd': 'startrecording',
            'sessionid': str(self.sessionid),
            'mediapath': 'data',
            'duration': '%s' % str(recording_length),
            'fileprefix': '%s' % str(filename)
        }  # Needs work
        self.record = self.sendCMD(para)

    def stopRecording(self):
        para = {
            'cmd': 'stoprecording',
            'sessionid': str(self.sessionid)
        }
        self.record = self.sendCMD(para)

    def startScan(self):
        para = {
            'cmd': 'startscan',
            'sessionid': str(self.sessionid),
            'force': '1',
            'freqbwlist': self.frequencies,
            'location': 'Location1'
        }
        self.scan = self.sendCMD(para)

    def getScanStatus(self):
        para = {
            'cmd': 'getscanstatus',
            'sessionid': str(self.sessionid)
        }
        self.scan = self.sendCMD(para)['MML']['Body']['ScanStatus']
        print(self.scan)

    def stopScan(self):
        params = {
            'cmd': 'stopscan',
            'sessionid': str(self.sessionid),
            'discardservicesfound': '0',
            'eraseservicelist': '1'
        }
        self.scan = self.sendCMD(params)

    def downloadFirmware(self):
        url = 'http://cf.watchairtv.com/sys/'
        # need a way of getting this filename
        filename = 'WatchAir_sw_v1.9.1_1521007676.zip'
        response = requests.get(url + filename)
        file = open(filename, 'wb')
        file.write(response.content)
        file.close()
        self.firmware = xmltodict.parse(response.text)

    def upgradeFirmwarePrepare(self):
        para = {
            'cmd': 'upgradefirmwareprepare',
            'sessionid': str(self.sessionid)
        }
        self.firmware = self.sendCMD(para)

    def pushFile(self):
        params = {
            'cmd': 'pushfile',
            'sessionid': str(self.sessionid),
            'force': '1',
            'fullpath': 'data/firmware.zip'
        }
        self.firmware = self.sendCMD(params)

    def streamVideo(self, frequency):
        frequency = 533000000
        params = {
            'cmd': 'startstreamingdata',
            'sessionid': str(self.sessionid),
            'uniqueid': '53300301',
            'freq': '%s' % str(frequency),  # needs work to be dynamic
            'channeltsid': '187',
            'sourceId': '1',
            'force': '0',
            'tvbps': '5000000',
            'vpid': '49',
            'apid': '52',
            'apid2': '53',
            'tvresolution': '1280x720',
            'pretune': '0',
            'tvcontainer': 'ts',
            'tvfps': '30',
            'tabps': '128000',
            'tvcodec': 'h264',
            'tacodec': 'aac'
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


if __name__ == "__main__":
    WA_Antenna = API(sys.argv)
