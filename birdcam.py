import subprocess, time, socket, os, json, requests
from gpiozero import MotionSensor
from gpiozero import LED
from signal import pause
from time import sleep
from datetime import datetime

pictureNumber = 0
currentDate = datetime.now().date()

def loadSettings():
    with open('settings.json') as file:
        settings = json.load(file)
    return settings

def saveSettings(settings):
    with open("settings.json", 'w') as file:
        json.dump(settings, file)

def blinkStatusLED():
    print('blinking')
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)

def uploadPictures():
    imageDir = './capturedImages'
    url = 'https://cam.yolobird.com/send'
    for subdir, dirs, files in os.walk(imageDir):
        for file in files:
            filelocation = os.path.join(subdir, file)
            headers = {'name': file}
            upload = {'image' : open(filelocation, 'rb')}
            response = requests.post(url, files=upload, headers=headers)
            if(response.status_code == 200):
                print(file + ' was successfully uploaded')

def takePictures():
    global pictureNumber
    print('motion registered, taking pictures')
    for pictures in range(numberOfPicturesToTake):
        yellowLed.on()
        pictureNumber += 1
        filename = './capturedImages/' + getCurrentDateString() + '-' + str(pictureNumber).rjust(5, '0') + '.jpg'
        camera.capture(filename, format='jpeg', quality=50, thumbnail=None)
        sleep(secondsBetweenPictures) # the raspberry zero needs ~0.5 seconds to take and save a picture
        yellowLed.off()
    print('pictures taken, waiting for motion')

def getCurrentDateString():
    global currentDate
    global pictureNumber
    newDate = datetime.now().date()
    if (currentDate != newDate):
        currentDate = newDate
        pictureNumber = 0

    return str(currentDate.year) + '-' + str(currentDate.month).rjust(2, '0') + '-' + str(currentDate.day).rjust(2, '0')

# looking for wifi connection
wifiConnection = False
try:
    myIP = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
    wifiConnection = True
except Exception:
    myIP = "Can't find an IP"

print("loading settings")
settings = loadSettings()
print('setting up LED')
redLed = LED(settings['redLedPIN'])
yellowLed = LED(settings['yellowLedPIN'])
greenLed = LED(settings['greenLedPIN'])

if wifiConnection: 
    greenLed.on()
    print('WIFI mode')
    print('Uploading pictures')
    uploadPictures()
    print('starting server')
    server = subprocess.Popen(["sudo", "flask", "run", "--host=0.0.0.0", '--port=80'])
    print('starting stream')
    streaming = subprocess.Popen(["sudo", "service", "uv4l_raspicam", "start"])
    greenLed.off()
    # TODO: insert LED code to indicate local server is running

else:
    redLed.on()
    print('Offline mode')
    # stop streaming
    subprocess.Popen(["service", "uv4l_raspicam", "stop"])
    # TODO: insert LED code to indicate offline camera is running
    import picamera
    print('setting up motion sensor')
    pir = MotionSensor(settings['pirPIN'], queue_len=settings['pirQueue_len'], 
        sample_rate=settings['pirSample_rate'],threshold=settings['pirThreshold'])
    print('setting up camera')
    camera = picamera.PiCamera()
    camera.resolution = (settings['xResolution'], settings['yResolution'])
    camera.vflip = settings['vFlip']
    camera.hflip = settings['hFlip']
    camera.sharpness = settings['sharpness']
    camera.exposure_mode = settings['exposure_mode']
    camera.meter_mode = settings['meter_mode']
    camera.awb_mode = settings['awb_mode']
    numberOfPicturesToTake = settings['numberOfPicturesToTake']
    secondsBetweenPictures = settings['secondsBetweenPictures']
    
    pir.when_motion = takePictures
    redLed.off()
    pause()