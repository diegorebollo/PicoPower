import network
import utime

def connect(ssid, pwd):    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, pwd)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
        
    return wlan


def access_point(ssid):
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    ap.active(True)
    ap.config(essid=ssid)
    ap.config(max_clients=2)
    print(f'ap config: {ap.ifconfig()}')
    
    return ap


def wifi_scan(interface='None'):
    
    if interface == 'None':
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        wlan.active(True)    
        scan_list = wlan.scan()    
        wlan.active(False)
    else:
        scan_list = interface.scan()
        
    wifi_list = []
    
    for n in scan_list:
        wifi_list.append(n[0].decode())
        
    return wifi_list
    
