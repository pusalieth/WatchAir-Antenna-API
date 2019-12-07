import requests
import xmltodict
import secrets


class WEBCONRTOL:
    def __init__(self, ip_address, zipcode):
        self.device_address = 'http://' + ip_address + '/mml.do'
        self.email = secrets['email']
        self.user_name = secrets['user']
        self.ssid = secrets['ssid']
        self.password = secrets['password']
        self.api_key = secrets['api_key']
        self.zipcode = secrets['zipcode']
        self.connect()
        self.frequencies = ("57000000,6000000,"
                            "63000000,6000000,"
                            "69000000,6000000,"
                            "79000000,6000000,"
                            "85000000,6000000,"
                            "177000000,7000000,"
                            "183000000,7000000,"
                            "189000000,7000000,"
                            "195000000,7000000,"
                            "201000000,7000000,"
                            "207000000,7000000,"
                            "213000000,7000000,"
                            "473000000,7000000,"
                            "479000000,7000000,"
                            "485000000,7000000,"
                            "491000000,7000000,"
                            "497000000,7000000,"
                            "503000000,7000000,"
                            "509000000,7000000,"
                            "515000000,7000000,"
                            "521000000,7000000,"
                            "527000000,7000000,"
                            "533000000,7000000,"
                            "539000000,7000000,"
                            "545000000,7000000,"
                            "551000000,7000000,"
                            "557000000,7000000,"
                            "563000000,7000000,"
                            "569000000,7000000,"
                            "575000000,7000000,"
                            "581000000,7000000,"
                            "587000000,7000000,"
                            "593000000,7000000,"
                            "599000000,7000000,"
                            "605000000,7000000,"
                            "611000000,7000000,"
                            "617000000,7000000,"
                            "623000000,7000000,"
                            "629000000,7000000,"
                            "635000000,7000000,"
                            "641000000,7000000,"
                            "647000000,7000000,"
                            "653000000,7000000,"
                            "659000000,6000000,"
                            "665000000,6000000,"
                            "671000000,6000000,"
                            "677000000,6000000,"
                            "683000000,6000000,"
                            "689000000,7000000,"
                            "695000000,7000000,"
                            "701000000,6000000,"
                            "707000000,6000000,"
                            "713000000,6000000,"
                            "719000000,6000000,"
                            "725000000,6000000,"
                            "731000000,6000000,"
                            "737000000,6000000,"
                            "743000000,6000000,"
                            "749000000,6000000,"
                            "755000000,6000000,"
                            "761000000,6000000,"
                            "767000000,6000000,"
                            "773000000,6000000,"
                            "779000000,6000000,"
                            "785000000,6000000,"
                            "791000000,6000000,"
                            "797000000,6000000,"
                            "803000000,6000000")

    def sendCMD(self, PARAMS):
        response = requests.get(self.device_address, params=PARAMS)
        print(response.text)
        return xmltodict.parse(response.text)

    def connect(self):
        params = {'cmd': 'connect',
                  'clientid': 'Automated',
                  'force': '1',
                  'timeout': '86400',
                  'clientUserId': self.email,
                  'clientUserProfile': self.user_name}
        self.sessionid = self.sendCMD(params)['MML']['Body']['SessionID']

    def disconnect(self):
        para = {'cmd': 'disconnect',
                'sessionid': self.sessionid}
        self.sendCMD(para)

    def getHomeNetworks(self):
        para = {'cmd': 'gethomenetworks',
                'sessionid': self.sessionid}
        self.wifi = self.sendCMD(para)

    def setWiFiNetwork(self):
        params = {'cmd': 'addnetwork',
                  'sessionid': 'watchair',
                  'networkid': self.SSID,
                  'user': self.user_name,
                  'password': self.password,
                  'priority': '0'}
        self.wifi = self.sendCMD(params)

    def getStorageStatus(self):
        para = {'cmd': 'getmediapaths',
                'sessionid': 'watchair'}
        self.storage = self.sendCMD(
            para)['MML']['Body']['Devices']['MediaDevice']

    def getPVRFileList(self):
        para = {'cmd': 'getpvrfilelist',
                'sessionid': 'watchair'}
        self.pvr = self.sendCMD(para)['MML']['Body']['PVRFiles']['PVRFile']

    def getSignalStatus(self):
        para = {'cmd': 'getstatusall',
                'sessionid': self.sessionid}
        self.status = self.sendCMD(para)['MML']['Body']['SignalStatistics']

    def getINAmode(self):
        para = {'cmd': 'getInamode',
                'sessionid': self.sessionid}
        self.mode = self.sendCMD(para)
        print(self.status)

    def setINAmode(self):
        params = {'cmd': 'setInamode',
                  'sessionid': self.sessionid, 'mode': '1'}
        self.mode = self.sendCMD(params)

    def getDeviceInfo(self):
        para = {'cmd': 'getdeviceinfo',
                'sessionid': self.sessionid}
        self.device_info = self.sendCMD(para)['MML']['Body']['DeviceInfo']
        print(self.device_info)

    def getServiceInformationLists(self):
        para = {'cmd': 'getserviceinformationlists',
                'sessionid': self.sessionid, 'uniqueid': '53300301'}
        self.service = self.sendCMD(para)
        print(self.service)

    def startRecording(self):
        para = {'cmd': 'startrecording',
                'sessionid': self.sessionid,
                'mediapath': 'data',
                'duration': '2054',
                'fileprefix': '3TV+News+a...'}  # Needs work
        self.record = self.sendCMD(para)

    def stopRecording(self):
        para = {'cmd': 'stoprecording',
                'sessionid': self.sessionid}
        self.record = self.sendCMD(para)

    def startScan(self):
        para = {'cmd': 'startscan',
                'sessionid': self.sessionid,
                'force': '1',
                'freqbwlist': self.frequencies,
                'location': 'Location1'}
        self.scan = self.sendCMD(para)

    def getScanStatus(self):
        para = {'cmd': 'getscanstatus',
                'sessionid': self.sessionid}
        self.scan = self.sendCMD(para)['MML']['Body']['ScanStatus']
        print(self.scan)

    def stopScan(self):
        params = {'cmd': 'stopscan',
                  'sessionid': self.sessionid,
                  'discardservicesfound': '0',
                  'eraseservicelist': '1'}
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
        para = {'cmd': 'upgradefirmwareprepare',
                'sessionid': self.sessionid}
        self.firmware = self.sendCMD(para)

    def pushFile(self):
        params = {'cmd': 'pushfile',
                  'sessionid': self.sessionid,
                  'force': '1',
                  'fullpath': 'data/firmware.zip'}
        self.firmware = self.sendCMD(params)

    def streamVideo(self):
        params = {'cmd': 'startstreamingdata',
                  'sessionid': self.sessionid,
                  'uniqueid': '53300301',
                  'freq': '533000000',  # needs work to be dynamic
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
                  'tacodec': 'aac'}
        self.video_stream = self.sendCMD(params)

    def getArtwork(self):
        self.asset_name = 'p10005060_st_h13_ac' + \
            '.jpg'  # this probably changes and needs work
        url = 'http://epic.tmsimg.com/assets/' + self.asset_name
        PARAMS = {'w': '240',
                  'h': '135'}
        response = requests.get(url, params=PARAMS)
        print(response.text)
        return xmltodict.parse(response.text)

    def getLineup(self):
        url = 'http://data.tmsapi.com/v1.1/lineups/USA-OTA' + self.zipcode + '/grid'
        PARAMS = {'stationId': '66570',  # don't know what these values mean, and probably need work
                  'startDateTime': '2019-12-06T03:00Z',
                  'endDateTime': '2019-12-06T04-00Z',
                  'imageSize': 'Sm',
                  'imageAspectTV': '16x9',
                  'api_key': self.api_key}
        response = requests.get(url, params=PARAMS)
        print(response.text)
        return xmltodict.parse(response.text)


if __name__ == "__main__":
    WA_Antenna = WEBCONRTOL('192.168.1.143', '85024')
    WA_Antenna.connect()