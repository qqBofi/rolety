import board
import busio
import digitalio
import time
import adafruit_requests as requests
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
from adafruit_wsgi.wsgi_app import WSGIApp
import adafruit_wiznet5k.adafruit_wiznet5k_wsgiserver as server
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
from shadectrl import shade
from sensors import myDHT
from sensors import myTime
from myhtml import myHtml
import sys

print("")
print("############")
print("Start Rolety")
print("############")

sensor = myDHT(board.GP15)
s1 = shade("L", board.GP0, board.GP1, board.GP2, board.GP3)
s2 = shade("R", board.GP4, board.GP5, board.GP6, board.GP7)
i, i2 = 0, 0

##SPI0
SPI0_SCK = board.GP18
SPI0_TX = board.GP19
SPI0_RX = board.GP16
SPI0_CSn = board.GP17

##reset
W5x00_RSTn = board.GP20

# Setup your network configuration below
# random MAC, later should change this value on your vendor ID
MY_MAC = (0xdd, 0xb0, 0xf1, 0x00, 0x00, 0x01)
IP_ADDRESS = (192, 168, 2, 211)
SUBNET_MASK = (255, 255, 255, 0)
GATEWAY_ADDRESS = (192, 168, 2, 1)
DNS_SERVER = (8, 8, 8, 8)

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
ethernetRst.direction = digitalio.Direction.OUTPUT

# For Adafruit Ethernet FeatherWing
cs = digitalio.DigitalInOut(SPI0_CSn)

# cs = digitalio.DigitalInOut(board.D5)
spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)

# Reset W5500 first
ethernetRst.value = False
time.sleep(1)
ethernetRst.value = True

# Initialize ethernet interface without DHCP
eth = WIZNET5K(spi_bus, cs, is_dhcp=False, mac=MY_MAC, debug=False)
# Initialize ethernet interface with DHCP
# eth = WIZNET5K(spi_bus, cs, is_dhcp=True, mac=MY_MAC, debug=False)

# Set network configuration
eth.ifconfig = (IP_ADDRESS, SUBNET_MASK, GATEWAY_ADDRESS, DNS_SERVER)

myip = eth.pretty_ip(eth.ip_address)
print("Chip:", eth.chip)
print("MAC :", eth.pretty_mac(eth.mac_address))
print("IP  :", myip)

# Initialize a requests object with a socket and ethernet interface
try:
    requests.set_socket(socket, eth)
    html = myHtml("Alex", eth)
    timer = myTime(socket)
except:
    print('Failed with sockets')

# Here we create our application, registering the
# following functions to be called on specific HTTP GET requests routes
try:
    web_app = WSGIApp()
except:
    print('Failed with WSGIApp')

#HTTP Request handlers
@web_app.route("/led_on")
def led_on(request):  # pylint: disable=unused-argument
    print("LED on!")
    led.value = True
    htmls = html.build_response(i, i2, sensor, s1, s2, timer)
    return ("200 OK", [], [htmls])

@web_app.route("/led_off")
def led_off(request):  # pylint: disable=unused-argument
    print("LED off!")
    led.value = False
    htmls = html.build_response(i, i2, sensor, s1, s2, timer)
    return ("200 OK", [], [htmls])

@web_app.route("/shadeL_up")
def shadeL_up(request):
    global s1
    s1.shadeOpen()
    htmls = html.build_response(i, i2, sensor, s1, s2, timer)
    return ("200 OK", [], [htmls])

@web_app.route("/shadeL_down")
def shadeL_down(request):
    global s1
    s1.shadeClose()
    htmls = html.build_response(i, i2, sensor, s1, s2, timer)
    return ("200 OK", [], [htmls])

@web_app.route("/shadeL_smallGap")
def shadeL_smallGap(request):
    global s1
    s1.shadeSmallGap()
    htmls = html.build_response(i, i2, sensor, s1, s2, timer)
    return ("200 OK", [], [htmls])

@web_app.route("/shadeR_up")
def shadeR_up(request):
    global s2
    s2.shadeOpen()
    htmls = html.build_response(i, i2, sensor, s1, s2, timer)
    return ("200 OK", [], [htmls])

@web_app.route("/shadeR_down")
def shadeR_down(request):
    global s2
    s2.shadeClose()
    htmls = html.build_response(i, i2, sensor, s1, s2, timer)
    return ("200 OK", [], [htmls])

@web_app.route("/shadeR_smallGap")
def shadeR_smallGap(request):
    global s2
    s2.shadeSmallGap()
    htmls = html.build_response(i, i2, sensor, s1, s2, timer)
    return ("200 OK", [], [htmls])

@web_app.route("/data")
def getdata(request):
    htmls = html.build_data(i, i2, sensor, s1, s2, timer)
    return ("200 OK", [], [htmls])

@web_app.route("/reset")
def getdata(request):
    htmls = html.build_reset()
    return ("200 OK", [], [htmls])

@web_app.route("/setLclosed")
def shadeLisclosed(request):
    s1.shadeReset("isclosed")
    htmls = html.build_response(i, i2, sensor, s1, s2, timer)
    return ("200 OK", [], [htmls])

@web_app.route("/setLopen")
def shadeLisopen(request):
    s1.shadeReset("isopen")
    htmls = html.build_response(i, i2, sensor, s1, s2, timer)
    return ("200 OK", [], [htmls])

@web_app.route("/setRclosed")
def shadeRisclosed(request):
    s2.shadeReset("isclosed")
    htmls = html.build_response(i, i2, sensor, s1, s2, timer)
    return ("200 OK", [], [htmls])

@web_app.route("/setRopen")
def shadeRisopen(request):
    s2.shadeReset("isopen")
    htmls = html.build_response(i, i2, sensor, s1, s2, timer)
    return ("200 OK", [], [htmls])

@web_app.route("/")
def root(request):  # pylint: disable=unused-argument
    #print("Root WSGI handler")
    htmls = html.build_response(i, i2, sensor, s1, s2, timer)
    # return ("200 OK", [], ["Root document"])
    return ("200 OK", [], [htmls])

# Here we setup our server, passing in our web_app as the application
try:
    server.set_interface(eth)
    wsgiServer = server.WSGIServer(80, application=web_app)
except:
    print('Failed with WsgiServer Creation')

# Start the server
serverOK = False
try:
    wsgiServer.start()
    serverOK = True
except:
    print('Failed with WsgiServer Start')

while True:
    # Could do any other background tasks here, like reading sensors
    s1.shadeMove()
    s2.shadeMove()
    try:
        if eth.link_status:
            wsgiServer.update_poll()
    except:
        print('Wsgi upd NOK ', end='')

    try: timer

    except NameError: timer = None

    i = i + 1
    if i % 60 == 0:
        sensor.get_temperature()
    if i % 10 == 0 and eth.link_status:
        timer.resync()
    if i % 3 == 0:
        if timer is None:
            tnow = ''
        else:
            tnow = timer.now()
        print( "{} {} {}  *  {}  *  {} * eth:{}".format(tnow, i, i2, s1.outstr(), s2.outstr(), eth.link_status) )
    if i > 1001:
        i = 0
        i2 = i2 + 1
    time.sleep(1.0)


