# Birdcam by BirdsOnBikes
## Anleitung

### Die Komponenten

#### RaspberryPi 3
<img src="assets-README/Raspi.png" width="200">

#### Raspberry Kamera V.2
<img src="assets-README/Kamera.png" width="200">

#### PIR Sensor (Bewegungssensor)
<img src="assets-README/PIRSensor.png" width="200">

#### 3x Kabel Weiblich/ Weiblich
<img src="assets-README/Kabel.png" width="200">

### Zusammenbauen der Komponenten

    1. Den Gehäusedecke des Raspberry Pi´s abnehmen. 

    2. Das Kabel des Kamermoduls in den Beschrifteten Kamera Eingang stecken.
    (Hier auf die Richtung der Kontakte achten)

    3. Drei Kabel an die Pins (GND, VCC, SIG) des PIR Sensors anschließen. 

    4. Die Kabel müssen nun jeweils richtig an die Pins des Raspberry Pi´s angeschlossen werden. 
    GND = 6 / VCC = 4 / SIG = 16

<img src="assets-README/GPIO.png">


### Installation

* [Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit) auf SD-Karte geflasht
* WLAN-Konfigurieren und SSH aktivieren:
  * Speicherkarte in deinen Rechner einlegen
  * auf "boot" eine Datei mit dem Namen `ssh` und eine Datei``wpa_supplicant.conf`` anlegen
  * ``wpa_supplicant.conf`` Editor öffnen und folgenden Code eingeben:
```bash ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
country=de
update_config=1
network={
    ssid="<Name of your wireless LAN>"
    psk="<Password for your wireless LAN>"
}
```
* [Quelle](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)
* jetzt den Raspberry starten
* per SSH auf Raspberry zugreifen
* Das Repository der Streaming Library UV4L hinzufügen
* `curl https://www.linux-projects.org/listing/uv4l_repo/lpkey.asc | sudo apt-key add -`
* `echo 'deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch main' | sudo tee -a /etc/apt/sources.list`
* `sudo apt update`
* `sudo apt full-upgrade`
* Die benötigten Libraries installieren
* `sudo apt install python3-picamera python3-pip python3-gpiozero python3-pip uv4l uv4l-raspicam uv4l-raspicam-extras uv4l-webrtc`
* Kamera in raspi-config aktivieren
* `sudo raspi-config`
* (optional) den Hostname des Raspberry Pi
* git clone https://github.com/christian-busse/birdcam
* im Verzeichnis birdcam den folgenden Befehl ausführen:
``` bash
nohup python3 birdcam.py >output.log >error.log &
```
* jetzt kann man die SSH-Verbindung zum Raspberry mit ```exit``` wieder schließen
* um das Birdcam-Programm bei jedem Start auszuführen, bitte diese [Anleitung](https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/method-1-rclocal) befolgen
