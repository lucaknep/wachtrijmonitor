# Wachtrijmonitor – Lake Side Mania

**BC1a Hardware Interfacing | Luca Knepper | S1509628**

---

## Beschrijving

Dit project is een prototype van een wachtrijmonitorsysteem voor de wildwaterbaan van attractiepark Lake Side Mania. Het systeem meet automatisch hoeveel mensen er in de wachtrij staan en geeft de status aan via gekleurde LEDs en een buzzer.

## Hardware

| Component | Pin |
|---|---|
| HC-SR04 (Trig) | GP1 |
| HC-SR04 (Echo) | GP2 |
| LED rood | GP36 |
| LED geel | GP37 |
| LED groen | GP18 |
| Buzzer | GP38 |

## Hoe werkt het?

Bij het opstarten kalibreeert de sensor automatisch de lege afstand. Daarna telt het systeem personen die dichterbij komen dan normaal.

| Status | LED | Betekenis |
|---|---|---|
| GROEN | Groen | Wachtrij normaal (< 10 personen) |
| GEEL | Geel | Druk – medewerker oproepen (10-19 personen) |
| ROOD | Rood + buzzer | Kritiek – wachtrijgrens bereikt (20+ personen) |

Elke 32 seconden arriveert een bootje en gaan er 6 personen van de teller af.

## Opstarten

1. Sluit de ESP32-S3 Pico aan via USB-C
2. Zorg dat niemand voor de sensor staat tijdens het opstarten
3. Het systeem kalibreeert automatisch en start daarna op

## Board

ESP32-S3 Pico met MicroPython firmware
