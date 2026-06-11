import machine
import utime

# --- INSTELLINGEN ---
GELE_DREMPEL    = 10     # Bij hoeveel personen wordt de status GEEL?
RODE_DREMPEL    = 20     # Bij hoeveel personen wordt de status ROOD?
BOOTJE_INTERVAL = 32     # Hoeveel seconden tussen twee bootjes?
VERSCHIL_CM     = 15     # Hoeveel cm dichter dan normaal = iemand gedetecteerd?
DEBOUNCE_MS     = 2000   # Hoelang wachten na een detectie? (voorkomt dubbele tellingen)

# --- PINNEN ---
trig      = machine.Pin(1,  machine.Pin.OUT)
echo      = machine.Pin(2,  machine.Pin.IN)
led_rood  = machine.Pin(36, machine.Pin.OUT)
led_geel  = machine.Pin(37, machine.Pin.OUT)
led_groen = machine.Pin(18, machine.Pin.OUT)
buzzer    = machine.Pin(38, machine.Pin.OUT)

# --- VARIABELEN ---
wachtrij         = 0
status           = "GROEN"
laatste_detectie = 0
laatste_bootje   = utime.ticks_ms()
rustige_afstand  = 0


# --- AFSTAND METEN ---
def meet_afstand():
    trig.value(0)
    utime.sleep_us(2)
    trig.value(1)
    utime.sleep_us(10)
    trig.value(0)
    try:
        duur = machine.time_pulse_us(echo, 1, 30000)
    except:
        return 999
    # Negatieve of nul waarde = foutmeting, negeer die
    if duur <= 0:
        return 999
    return duur / 58


# --- KALIBRATIE BIJ OPSTARTEN ---
# Meet 10x de lege afstand zodat het systeem weet wat normaal is
print("Kalibreren... zorg dat niemand voor de sensor staat!")
utime.sleep_ms(2000)
metingen = []
for i in range(10):
    meting = meet_afstand()
    if meting < 999:
        metingen.append(meting)
    utime.sleep_ms(200)
rustige_afstand = sum(metingen) / len(metingen)
print("Klaar! Normale afstand:", round(rustige_afstand, 1), "cm")
print("==============================================")


# --- HOOFDLUS ---
while True:

    # 1. Meet de afstand
    afstand = meet_afstand()
    nu = utime.ticks_ms()

    # 2. Iemand gedetecteerd?
    # Alleen tellen als afstand veel kleiner is dan de normale afstand
    if afstand < (rustige_afstand - VERSCHIL_CM):
        if utime.ticks_diff(nu, laatste_detectie) > DEBOUNCE_MS:
            wachtrij = wachtrij + 1
            laatste_detectie = nu
            print("Persoon gedetecteerd! Wachtrij:", wachtrij)

    # 3. Bootje aangekomen?
    if utime.ticks_diff(nu, laatste_bootje) >= BOOTJE_INTERVAL * 1000:
        wachtrij = max(0, wachtrij - 6)
        laatste_bootje = utime.ticks_ms()
        print("Bootje weg! Wachtrij:", wachtrij)

    # 4. Bereken de geschatte wachttijd (FR4)
    wachttijd_minuten = round((wachtrij / 6) * BOOTJE_INTERVAL / 60, 1)

    # 5. Welke LED moet aan en wat is de status?
    led_rood.value(0)
    led_geel.value(0)
    led_groen.value(0)
    buzzer.value(0)

    if wachtrij >= RODE_DREMPEL:
        led_rood.value(1)
        if status != "ROOD":
            # Net naar ROOD gegaan: buzzer 6x piepen
            for i in range(6):
                buzzer.value(1)
                utime.sleep_ms(500)
                buzzer.value(0)
                utime.sleep_ms(200)
            laatste_bootje = utime.ticks_ms()  # reset bootje timer
        status = "ROOD"

    elif wachtrij >= GELE_DREMPEL:
        led_geel.value(1)
        if status != "GEEL":
            laatste_bootje = utime.ticks_ms()  # reset bootje timer
        status = "GEEL"

    else:
        led_groen.value(1)
        status = "GROEN"

    # 6. Print de situatie in de console (FR3 + FR4)
    print("Wachtrij:", wachtrij, "| Status:", status,
          "| Interval:", BOOTJE_INTERVAL, "s | Wachttijd:", wachttijd_minuten, "min")

    utime.sleep_ms(500)
