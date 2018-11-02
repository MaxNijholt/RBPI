from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
import os

# STATUSLED = 40
STATUSLED   = 7 #rood
STATUSDRUP1 = 22 #bruin
STATUSDRUP2 = 18 #zwart
STATUSCAM   = 16 #lichtgrijs
SWITCHDRUP  = 15 #grijs
SWITCHCAM   = 13 #paars
INPUTSW1    = 11 #blauw
INPUTSW2    = 12 #groen

# timing_druppel1 = 0.0400    # druppel 1 tijd dat het klepje open staat
# timing_druppel2 = 0.0400    # druppel 2 tijd dat het klepje open staat

# timing_tussen1  = 0.0600    # tijd tussen druppel 1 en druppel 2
# timing_tussen2  = 0.2000    # tijd tot de camera een signaal krijgt   (samen 0.24 / 0.26

# timing_flash    = 0.0200    # Duur van het signaal om de camera een foto te laten maken.
# timing_pauze    = 7.0000    # Pause tijd waarop het water weer rustig is en de volgende druppels kunnen komen
ontluchten      = 0.5000    # opstarten en laat 1/2 seconde water stromen

def cls():
   os.system('clear')

def init():
    cls()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    GPIO.setup(STATUSLED, GPIO.OUT)
    GPIO.setup(STATUSDRUP1, GPIO.OUT)
    GPIO.setup(STATUSDRUP2, GPIO.OUT)
    GPIO.setup(STATUSCAM, GPIO.OUT)
    GPIO.setup(SWITCHDRUP, GPIO.OUT)
    GPIO.setup(SWITCHCAM, GPIO.OUT)
    # GPIO.setup(INPUTSW1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(INPUTSW2, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    GPIO.output(STATUSLED, GPIO.LOW)         # LED opstelling actief
    GPIO.output(STATUSDRUP1, GPIO.LOW)       # LED druppel 1
    GPIO.output(STATUSDRUP2, GPIO.LOW)       # LED druppel 2
    GPIO.output(STATUSCAM, GPIO.LOW)         # LED Camera
    GPIO.output(STATUSDRUP1, GPIO.HIGH)      # Trigger Camera

    GPIO.output(SWITCHDRUP, GPIO.LOW)                # Trigger Magneetklep
    print("Ontluchten waterklep")
    time.sleep(ontluchten)
    GPIO.output(SWITCHDRUP, GPIO.HIGH)               # Trigger Magneetklep

def druppel1(timing):
    print("Druppel 1 aan voor %.4f seconden" % timing)
    GPIO.output(STATUSDRUP1, GPIO.HIGH)
    GPIO.output(SWITCHDRUP, GPIO.LOW)
    time.sleep(timing)
    GPIO.output(SWITCHDRUP, GPIO.HIGH)
    GPIO.output(STATUSDRUP1, GPIO.LOW)
    print("Druppel 1 uit")

def druppel2(timing):
    print("Druppel 2 aan voor %.4f seconden" % timing)
    GPIO.output(STATUSDRUP2, GPIO.HIGH)
    GPIO.output(SWITCHDRUP, GPIO.LOW)
    time.sleep(timing)
    GPIO.output(SWITCHDRUP, GPIO.HIGH)
    GPIO.output(STATUSDRUP2, GPIO.LOW)
    print("Druppel 2 uit")

def flash(timing):
    print("Camera in ")
    GPIO.output(STATUSCAM, GPIO.HIGH)
    GPIO.output(SWITCHCAM, GPIO.LOW)
    time.sleep(timing)
    GPIO.output(SWITCHCAM, GPIO.HIGH)
    GPIO.output(STATUSCAM, GPIO.LOW)
    print("Camera uit")

app = Flask(__name__)

init()

@app.route("/", methods=['POST','GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        cls()
        try:
            # value = float(request.form['amount'])
            timing_druppel1 = float(request.form['timing_druppel1'])   # druppel 1 tijd dat het klepje open staat
            timing_druppel2 = float(request.form['timing_druppel2'])   # druppel 2 tijd dat het klepje open staat
            timing_tussen1  = float(request.form['timing_tussen1'])   # tijd tussen druppel 1 en druppel 2
            timing_tussen2  = float(request.form['timing_tussen2'])   # tijd tot de camera een signaal krijgt   (samen 0.24 / 0.26
            timing_flash    = float(request.form['timing_flash'])      # Duur van het signaal om de camera een foto te laten maken.
            timing_pauze    = float(request.form['timing_pauze'])      # Pause tijd waarop het water weer rustig is en de volgende
            exacutetimes    = int(request.form['exacutetimes'])

            print("Timing drup1: {}\n Timing drup2: {}\n Timing tussen1: {}\n Timing tussen2: {}\n Timing flash: {}\n Timing pauze: {}\n Aantal loops: {}".format(timing_druppel1,
                timing_druppel2,
                timing_tussen1,
                timing_tussen2,
                timing_flash,
                timing_pauze,
                exacutetimes))
            try:
                for i in range(0, exacutetimes):
                    GPIO.output(STATUSLED, GPIO.HIGH)
                    print("Druppelaar nieuwe loop")
                    druppel1(timing_druppel1)
                    time.sleep(timing_tussen1)
                    print("Druppelaar nieuwe loop")
                    druppel2(timing_druppel2)
                    time.sleep(timing_tussen2)
                    flash(timing_flash)
                    print("Sleeping")
                    GPIO.output(STATUSLED, GPIO.LOW)
                    time.sleep(timing_pauze)
            except:
                print("except")
                pass
            # GPIO.output(STATUSLED, GPIO.LOW)
        except:
            print('Exception')
            pass
        return render_template('index.html', 
            timing_druppel1=timing_druppel1, 
            timing_druppel2=timing_druppel2,
            timing_tussen=timing_tussen1,
            timing_tussen2=timing_tussen2,
            timing_flash=timing_flash,
            timing_pauze=timing_pauze)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')