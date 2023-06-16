import datetime
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import requests
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep
import cv2
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Raspberry Pi pin configuration:
RST = 24
#Setting the GPIO for the sensor.
R = 10
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(R, GPIO.IN)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(20, GPIO.HIGH)

gauth = GoogleAuth()

drive = GoogleDrive(gauth)

def picture():
    B=1
    K=1
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if(K==1):

        while B == 1:
            cv2.waitKey(1)
            ret, pic = cap.read()
            #pic = cv2.cvtColor(pic, cv2.COLOR_RGB2GRAY)
            #pic = cv2.convertScaleAbs(pic, alpha=4 , beta=-4)
            cv2.imshow("Picture", pic)
            if GPIO.input(21) == 1:
                cv2.imwrite("word.jpg", pic)
                B = 2
                cap.release()
                cv2.destroyAllWindows()
                upload_file = 'word.jpg'
                gfile= drive.CreateFile({'parents':[{'id': '1d-vlp_CJnSjtslRSY3Mh2P26ZsNq2uSY'}]})
                #Read file and set it as the content of this instance.
                gfile.SetContentFile(upload_file)
                gfile.Upload() #Upload the file
                print("Uploaded")
                # 1. Retrieve file list from the specific folder.
                fileList = drive.ListFile({'q': " '1d-vlp_CJnSjtslRSY3Mh2P26ZsNq2uSY' in parents"}).GetList()
                for file in fileList:
                    print('Title: %s, ID: %s' % (file['title'], file['id']))
                    time.sleep(2)
                    drive.CreateFile({'id': file['id']}).Delete()
                time.sleep(2.5)
                fileList = drive.ListFile({'q': " '1d-vlp_CJnSjtslRSY3Mh2P26ZsNq2uSY' in parents"}).GetList()

                for file in fileList:
                        print('Title: %s, ID: %s' % (file['title'], file['id']))
                        MSD = file['id']
                try:
                    file_obj = drive.CreateFile({'id': MSD})
                    file_obj.GetContentFile('text.txt')
                    time.sleep(2)
                    f = open('text.txt', 'r')
                    file_contents = f.read()
                    print(file_contents)
                    return file_contents,3,1

                except:
                    return "Tekrar Deneyin",3,1
                    pass
                
            if (GPIO.input(R) == 0):
                cap.release()
                cv2.destroyAllWindows()
                B = 2
                K = 2
                time.sleep(0.1)
                return " ",0,2


def weekday(a):

    if(a==0):
        return " Pazartesi"
    if(a==1):
        return "           Sali"
    if(a==2):
        return " Carsamba"
    if(a==3):
        return " Persembe"
    if(a==4):
        return "         Cuma"
    if(a==5):
        return " Cumartesi"
    if(a==6):
        return "        Pazar"

    
 



# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)


# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))


# Load image based on OLED display height.  Note that image is converted to 1 bit color.
image = Image.open('Final3.ppm').convert('1')


# Alternatively load a different format image, resize it, and convert to 1 bit color.
#image = Image.open('happycat.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')

# Display image.
disp.image(image)
disp.display()

# Make blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load default font.
#font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('BMarmy.TTF', 12)
draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.text((17,27),"Hosgeldiniz",font=font, fill=255)
time.sleep(1.5)
disp.image(image)
disp.display()
time.sleep(1.5)

def jprint(obj):
	text = json.dumps(obj, sort_keys=True , indent=4)
	print(text)

response = requests.get("https://api.openweathermap.org/data/2.5/find?q=Ankara&units=metric&appid=7e0d145d3a696ff777f00fb0d5280b7f")
weather = response.json()
response = requests.get("https://api.exchangerate.host/latest?&base=USD")
currencyUSD = response.json()
response = requests.get("https://api.exchangerate.host/latest?&base=EUR")
currencyEUR = response.json()
response = requests.get("https://api.exchangerate.host/latest?&base=GBP")
currencyGBP = response.json()

city = str(weather['list'][0]['name'])
celcius = str(weather['list'][0]['main']['temp'])
basic = str(weather['list'][0]['weather'][0]['main'])
detail = str(weather['list'][0]['weather'][0]['description'])

USD = str(float('%.2f'% currencyUSD['rates']['TRY']))
EUR = str(float('%.2f'% currencyEUR['rates']['TRY']))
GBP = str(float('%.2f'% currencyGBP['rates']['TRY']))

print(city)
print(celcius)
print(basic)
print(detail)

print("1 USD = ",USD, "TRY")
print("1 EUR = ",EUR, "TRY")
print("1 GBP = ",GBP, "TRY")


count = 1
A = 0
start_time = time.time()

while count == 1:
    
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time > 120:
        start_time = time.time()
        response = requests.get("https://api.openweathermap.org/data/2.5/find?q=Ankara&units=metric&appid=7e0d145d3a696ff777f00fb0d5280b7f")
        weather = response.json()
        response = requests.get("https://api.exchangerate.host/latest?&base=USD")
        currencyUSD = response.json()
        response = requests.get("https://api.exchangerate.host/latest?&base=EUR")
        currencyEUR = response.json()
        response = requests.get("https://api.exchangerate.host/latest?&base=GBP")
        currencyGBP = response.json()
        

        city = str(weather['list'][0]['name'])
        celcius = str(weather['list'][0]['main']['temp'])
        basic = str(weather['list'][0]['weather'][0]['main'])
        detail = str(weather['list'][0]['weather'][0]['description'])

        USD = str(float('%.2f'% currencyUSD['rates']['TRY']))
        EUR = str(float('%.2f'% currencyEUR['rates']['TRY']))
        GBP = str(float('%.2f'% currencyGBP['rates']['TRY']))

        print(city)
        print(celcius)
        print(basic)
        print(detail)

        print("1 USD = ",USD, "TRY")
        print("1 EUR = ",EUR, "TRY")
        print("1 GBP = ",GBP, "TRY")

        draw.rectangle((0,0,width,height), outline=0, fill=0)
        disp.image(image)
        disp.display()
        

    
    if(GPIO.input(R) == 0):
        A = A + 1
        if(A == 4):
            A = 0
        time.sleep(0.1)

    


    if( A == 0 ):
        
        font = ImageFont.truetype('BMarmy.TTF', 12)
        now = datetime.datetime.now()
        weekofday = weekday(datetime.datetime.today().weekday())
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((60,0),now.strftime("%H.%M.%S"),font=font, fill=255)
        draw.text((40,55),now.strftime("%d.%m.%Y"),font=font, fill=255)
        draw.text((40,40),weekofday,font=font, fill=255)
        disp.image(image)
        disp.display()

        
    if( A == 1 ):
        
        font = ImageFont.truetype('BMarmy.TTF', 12)
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((0,0),"1USD= " + USD + " TRY",font=font, fill=255)
        draw.text((0,15),"1EUR= " + EUR + " TRY",font=font, fill=255)
        draw.text((0,30),"1GBP= " + GBP+  " TRY",font=font, fill=255)

        disp.image(image)
        disp.display()

    if( A == 2 ):
        font = ImageFont.truetype('BMarmy.TTF', 12)
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((0,0),city,font=font, fill=255)
        draw.text((0,15),celcius+ "'C",font=font, fill=255)
        draw.text((0,30),basic,font=font, fill=255)
        font = ImageFont.truetype('pixChicago.ttf', 9)
        draw.text((0,45),detail,font=font, fill=255)

        disp.image(image)
        disp.display()

    if( A == 3 ):
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        disp.image(image)
        disp.display()
        C = 1
        while C==1:
                word = picture()
                print(word)
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                disp.image(image)
                disp.display()
                try:
                    font = ImageFont.truetype('pixChicago.ttf', 10)
                    draw.text((0,25),word[0],font=font, fill=255)
                    disp.image(image)
                    disp.display()
                except:
                    pass
                A = word[1]
                C = word[2]
                

                

        
                        
              
           
                
                

                        
                        
                  
                                
                
                
        
        
        
        



        

