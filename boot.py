from microdot.microdot_asyncio import Microdot, Response, redirect, send_file
from microdot.microdot_utemplate import render_template
from file_manager import get_last_record, read_file, save_file
from wifi.wifi import connect, access_point, wifi_scan
from control import Relay, LedStatus
from machine import reset, WDT
from uping import uping
import utime
import uasyncio

VAR_FILE = 'config.json'
IS_PINGING = None

# Vars from File
INITIAL_CONFIG = None
PIN_RELAY = None
IP = None
PING_INTERVAL = None
WIFI_SSID = None
WIFI_PASSWORD = None
AUTO_TURN_ON = None

# Status LED
led = LedStatus()
led.turn_on(1)


# Reads Vars from File
def update_vars():
    
    global PIN_RELAY, IP, PING_INTERVAL, INITIAL_CONFIG, WIFI_SSID, WIFI_PASSWORD, AUTO_TURN_ON

    vars_json = read_file(VAR_FILE)
    utime.sleep(1)

    PIN_RELAY = vars_json['pin_relay']
    IP = vars_json['ip']
    PING_INTERVAL = vars_json['ping_interval'] * 60 * 1000
    INITIAL_CONFIG = eval(vars_json['initial_config'])
    WIFI_SSID = vars_json['ssid']
    WIFI_PASSWORD = vars_json['password']
    AUTO_TURN_ON = eval(vars_json['auto_turn_on'])
    
    
    
update_vars()


# Watchdog
wdt = WDT(timeout=PING_INTERVAL * 2)


# Wifi
if INITIAL_CONFIG:
    try:
        wlan = connect(WIFI_SSID, WIFI_PASSWORD)
    except OSError:
        led.turn_on(5)
        print('waiting for wifi')
        utime.sleep(300)
        wlan = connect(WIFI_SSID, WIFI_PASSWORD)
else:
    initial_wifi_list = wifi_scan()
    ap = access_point('PicoPower')
    led.on()


async def reset_machine():
    await uasyncio.sleep_ms(2 * 1000)
    reset()

utime.sleep(2)

# Relay
switch = Relay(PIN_RELAY)

# Ping to device


def is_pinging():
    global IS_PINGING
        
    gc.collect()
    wdt.feed()
    led.turn_on(1)

    if wlan.isconnected():
        try:
            ping = uping.ping(IP, quiet=True)
        except OSError:
            IS_PINGING = False
        else:
            if ping[1] > 0:
                IS_PINGING = True
            else:
                IS_PINGING = False
    else:
        print('no network')
        IS_PINGING = True

    return IS_PINGING

# Main Loop


async def main_loop():
    while AUTO_TURN_ON:
        if is_pinging():
            print(f'{IP} is ON')
            await uasyncio.sleep_ms(PING_INTERVAL)
        else:
            print(f'{IP} is OFF')
            await uasyncio.sleep_ms(PING_INTERVAL // 2)
            if not is_pinging():
                print(f'Turning ON {IP}')
                uasyncio.create_task(switch.on_off())
                await uasyncio.sleep_ms(90 * 1000)

# Web Server
app = Microdot()
Response.default_content_type = 'text/html'


@app.route('', methods=['GET'])
async def index(request):
    if INITIAL_CONFIG:
        last_run_time = get_last_record()
        return render_template('index.html', ip=IP, is_pinging=IS_PINGING, last_run_time=last_run_time, auto_turn_on=AUTO_TURN_ON)
    else:
        return redirect('/install')


@app.route('/install', methods=['GET', 'POST'])
async def install(request):

    if INITIAL_CONFIG:
        vars_file = read_file(VAR_FILE)
        
        wifi_list = wifi_scan(wlan)        
        ip = vars_file['ip']
        pin_relay = vars_file['pin_relay']
        ping_interval = vars_file['ping_interval']
        auto_turn_on = vars_file['auto_turn_on']

    else:
        wifi_list = initial_wifi_list
        ip = ''
        pin_relay = ''
        ping_interval = ''
        auto_turn_on = 'True'

    if request.method == 'POST':
        vars_file = read_file(VAR_FILE)

        vars_file['ssid'] = request.form['ssid']
        vars_file['password'] = request.form['password']
        vars_file['ip'] = request.form['ip']
        vars_file['pin_relay'] = int(request.form['pin'])
        vars_file['ping_interval'] = int(request.form['time'])
        vars_file['auto_turn_on'] = request.form['auto']
        vars_file['initial_config'] = 'True'
        
        save_file(VAR_FILE, vars_file)

        return redirect('/reboot')

    else:
        return render_template('install.html', wifi_list=wifi_list, ip=ip, ping_interval=ping_interval, pin_relay=pin_relay, auto_turn_on=auto_turn_on)


@app.route('/on-off', methods=['GET'])
async def on_off(request):
    uasyncio.create_task(switch.on_off())
    return redirect('/')


@app.route('/reset', methods=['GET'])
async def on_off(request):
    uasyncio.create_task(switch.reset())
    return redirect('/')


@app.route('/reboot', methods=['GET'])
async def reboot(request):
    uasyncio.create_task(reset_machine())
    return render_template('reboot.html')


@app.route('/history', methods=['GET'])
async def history_json(request):
    date_file = read_file('date_history.json')
    return date_file


@app.route('/static/<path:path>')
def static(request, path):
    if '..' in path:
        return 'Not found', 404
    return send_file('static/' + path)


@app.errorhandler(404)
async def not_found(request):
    return '<h2>404</h2>'


async def main():
    if INITIAL_CONFIG:
        uasyncio.create_task(main_loop())
        await app.run(debug=True, port=80)
    else:
        uasyncio.create_task(app.run(debug=True, port=80))


if __name__ == '__main__':
    uasyncio.run(main())

