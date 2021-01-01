# WatchAir-Antenna
Reverse Engineer of the Watch Air Antenna to use with a PC, Kodi, and other useful software

This API is still in testing state, but is confirmed to work for most functions.
The intent of this API is to allow control, and setup of the WatchAir Antenna from a PC, with no need or usage of an app.

(Update: 12/31/2020) Seems the original company went out of business. The lineup no longer works since it depended on gracenote services (which is a paid service). Looks like this software may be the only EOL support.

## Usage
Create a python script with a dictionary named vars, with the following variables given below. The password field is the password to your WiFi. The api key is linked to gracenote. You'll need to create a public account, and [register](https://developer.tmsapi.com) an application to get the api key.
```
vars = {
    'api_key': '',
    'email': '',
    'user': '',
    'ssid': '',
    'password': '',
    'zipcode': ''
}
```
Then, run the WA-API script followed by the function you want to use.
Example:
`python WA-API.py startScan`

## Device Details
* The device displays a directory listing on port 80, with /mnt/data, and ?/hls as the default uris. Streaming port is 8080. /mnt seems to be considered web root
* 7236.9 MiB capacity internal storage. Default 3.8 GiB used, with 3.9 MiB reserved. (Probably the MBR or EFI section)
* recordings stored at /mnt/data/media/recordings/
* DeviceId: `WA29D9C6` , DeviceModel: `EPUS-100W` 
* Uses `linux 3.4.39 #57` on firmware 1.9.1
* The WiFi interface is made by `Tabluae Limited`

### Backstory
To bad this thing failed, as it's pretty great in theory.
The problem is it was made to do something most people will never use it for (network ota tuner). Plus it was originally over price at $200. I bought it on sale at Fry's for $25.
I saw it received Over the Air TV, and somehow streamed it over WiFi/internet. I looked online, but there are zero APIs to use it for a wireless TV antenna for Kodi, or stream it as a DLNA stream, both the normal use cases for IP TV tuners.