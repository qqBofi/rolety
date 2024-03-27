class myHtml:
    def __init__(self, Name, eth):
        self.Name = Name
        self.hs = '''
<!DOCTYPE html>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<head>
<title>$TITLE</title>
<style>
.but {
  border: "1px";
  color: white;
  padding: 15px 10px;
  text-align: center;
  display: inline-block;
  font-size: 22px;
  font-weight: bold;
  margin: 4px 2px;
  cursor: pointer;
}

.butL {background-color: #ffffff; color: #020202 }
.butM {background-color: #888888;}
.butR {background-color: #444444;}
.butO {color: #020202; padding: 5px 5px;}
.butS {padding: 5px 5px; font-size: 15px; color: #020202 }

body {font-family: monaco, Consolas, "Lucida Console", monospace;}
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
  padding: 5px;
}
</style>
</head>
<body >
<div align="left">
<form>
$TEMP &nbsp; $HUMID</br>
</br>
Ľavá</br>
<button class="but butL" type="submit" formaction="/shadeL_up">↑</button>
<button class="but butM" type="submit" formaction="/shadeL_smallGap">=</button>
<button class="but butR" type="submit" formaction="/shadeL_down">↓</button>
&nbsp;
</br>
Pravá</br>
<button class="but butL" type="submit" formaction="/shadeR_up">↑</button>
<button class="but butM" type="submit" formaction="/shadeR_smallGap">=</button>
<button class="but butR" type="submit" formaction="/shadeR_down">↓</button>
&nbsp;
</br></br>
<button class="but butO" type="submit" formaction="/"> ← </button>
</br>
</br>
<a href="http://192.168.2.211/reset">reset po vypadku</a>
</br>
</form>
</br>
</br>
<table>
<tr>
<th>N</th>
<th>Stat real/des</th>
<th>in L/R</th>
<th>out L/R</th>
</tr>
$SW1
$SW2
</table>
</div>
</body>
</html>
'''
        self.hsReset = '''
<!DOCTYPE html>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<head>
<title>$TITLE</title>
<style>
.but {
  border: "1px";
  color: white;
  padding: 15px 10px;
  text-align: center;
  display: inline-block;
  font-size: 22px;
  font-weight: bold;
  margin: 4px 2px;
  cursor: pointer;
}

.butS {padding: 5px 5px; font-size: 15px; color: #020202 }

body {font-family: monaco, Consolas, "Lucida Console", monospace;}
</style>
</head>
<body >
<div align="left">
<form>
reset po vypadku
</br>
Lava
</br>
<button class="but butS" type="submit" formaction="/setLclosed">zatv</button>
<button class="but butS" type="submit" formaction="/setLopen">otv</button>
</br>
Prava
</br>
<button class="but butS" type="submit" formaction="/setRclosed">zatv</button>
<button class="but butS" type="submit" formaction="/setRopen">otv</button>
</br>
</form>
<a href="http://192.168.2.211">Naspet</a>
</div>
</body>
</html>
'''

        self.hsData = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>$TITLE</title>
</head>
<body>
<div align="left">
Temp:$TEMP<br>
Humid:$HUMID<br>
L:$LEFT<br>
R:$RIGHT<br>
</div>
</body>
</html>
'''
        self.hs = self.hs.replace("$CHIPNAME", eth.chip)
        self.hs = self.hs.replace("$IPADDRESS", eth.pretty_ip(eth.ip_address))
        self.html_string = self.hs.replace("$TITLE", Name)

    def build_response(self,i, i2, sensor, s1, s2, timer):
        htmls = self.html_string.replace("$I", "{}/{}".format(i, i2))
        htmls = htmls.replace("$TEMP", "{:.1f} °C".format(sensor.temperature_c))
        htmls = htmls.replace("$HUMID", "{:.1f} %".format(sensor.humidity))
        htmls = htmls.replace("$TIME", timer.now())
        htmls = htmls.replace("$SW1", s1.outhtm())
        htmls = htmls.replace("$SW2", s2.outhtm())
        return htmls

    def build_data(self,i, i2, sensor, s1, s2, timer):
        htmls = self.hsData.replace("$TEMP", "{:.1f}".format(sensor.temperature_c))
        htmls = htmls.replace("$HUMID", "{:.1f}".format(sensor.humidity))
        htmls = htmls.replace("$TITLE", self.Name)
        htmls = htmls.replace("$LEFT", "{}/{}".format(s1.real, s1.isOpen))
        htmls = htmls.replace("$RIGHT", "{}/{}".format(s2.real, s2.isOpen))
        return htmls

    def build_reset(self):
        htmls = self.hsReset
        return htmls
