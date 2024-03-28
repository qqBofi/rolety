[MD Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
# W5100S-EVB-Pico 
[WIZnet Document System](https://docs.wiznet.io/Product/iEthernet/W5100S/w5100s-evb-pico)

prve pripojenie
- stiahnut z [circuitpython.org](https://circuitpython.org/board/wiznet_w5100s_evb_pico/) .uf2 subor
- stlacit a drzat BOOTSEL (blizsie ku konektoru) a pripojit USB
- urobi to novy drive CIRCUITPY
- do neho skopirovat uf2 subor
- hotovo, uz len nakopirovat lib a programy


Zapojenie pinov:

* 1  GP0 lavy vypinac hore
* 2  GP1 lavy vypinac dole
* 4  GP2 lave rele hore (hnedy drot)
* 5  GP3 lave rele dole (cierny drot)

* 6  GP4 pravy vypinac hore
* 7  GP5 pravy vypinac dole
* 9  GP6 prave rele hore (hnedy drot)
* 10 GP7 prave rele dole (cierny drot)

* 19 GP14 volne
* 20 GP15 DHT senzor

* 18 GND
* 36 3v3

Spinace pripajaju zem, preto vstupy su digitalio.Pull.UP

Problem je max socket len 2, nevie obsluzit viac html klientov

Piny:
![schema](https://github.com/qqBofi/rolety/blob/master/doc/w5100s-evb-pico-1.1-pinout.png "Piny")

```python
# priklad kodu v MD
s = "Python syntax highlighting"
print s
```