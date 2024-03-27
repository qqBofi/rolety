import board
import time
import adafruit_dht
from rtc import RTC
import adafruit_ntp

class myTime:
    def __init__(self, socket):
        self.rtc = RTC()
        try:
            self.ntp = adafruit_ntp.NTP(socket, tz_offset=1)
            self.rtc.datetime = self.ntp.datetime
        except:
            self.rtc.datetime = datetime(2024, 04, 01, 00, 00)

    def now(self):
        n = "{:02}/{:02}/{:04} {:02}:{:02}:{:02}".format(
            self.rtc.datetime.tm_mday, self.rtc.datetime.tm_mon, self.rtc.datetime.tm_year,
            self.rtc.datetime.tm_hour, self.rtc.datetime.tm_min, self.rtc.datetime.tm_sec
        )
        return n

    def resync(self):
        try:
            self.rtc.datetime = self.ntp.datetime
        except:
            print('Failed with NTP')

        print(self.now())


class myDHT:
    def __init__(self, dht_pin):
        self.dhtDevice = adafruit_dht.DHT22(board.GP15)
        self.dhtDevice._trig_wait = 2000
        self.temperature_c = 0
        self.humidity = 0
        self.get_temperature()

    def get_temperature(self):
        try:
            self.temperature_c = self.dhtDevice.temperature
            self.humidity = self.dhtDevice.humidity
            print(
                "Temp: {:.1f} C    Humidity: {} % ".format(
                    self.temperature_c, self.humidity
                )
            )
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
        except Exception as error:
            self.dhtDevice.exit()
            # raise error

