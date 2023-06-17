# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


#Be sure to have installed all the missing packages.
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

# Raspberry Pi pin configuration for RST pin that will be used by the Toled :
RST = 4
# Setting the GPIO for the sensor.
R = 10
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(R, GPIO.IN)
# These are for the buttons so that it will work when pressed down
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.output(20, GPIO.HIGH)
# This is for setting your drive in the code, remember you need to have the credentials.json
# in the same directory as where this code is. You can search online how you can access to your Google Drive from python via API
# You can check this youtube video about it: https://www.youtube.com/watch?v=2mnKE9IERt4
# you may also need a settings.yaml file if you don't want to authenticate each time for google drive. You search online to learn more about it.
gauth = GoogleAuth()

drive = GoogleDrive(gauth)
# This is the function where we take a picture and send it to drive.
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
	    # Use these do change camera settings	
            #pic = cv2.cvtColor(pic, cv2.COLOR_RGB2GRAY)
            #pic = cv2.convertScaleAbs(pic, alpha=4 , beta=-4)
            cv2.imshow("Picture", pic)
            if GPIO.input(21) == 1: #This is when we press the button to take the picture of the word.
                cv2.imwrite("word.jpg", pic)
                B = 2
                cap.release()
                cv2.destroyAllWindows()
                upload_file = 'word.jpg'
		#For the ID basically in the URL of where you want to store, 
		#after the "https://drive.google.com/drive/folders/" part you have an id (the location of where the drive folder is at in your drive)
                gfile= drive.CreateFile({'parents':[{'id': 'your drive id '}]})
                #Read file and set it as the content of this instance.
                gfile.SetContentFile(upload_file)
                gfile.Upload() #Upload the file
                print("Uploaded")
                # Retrieve file list from the specific folder.
                fileList = drive.ListFile({'q': " 'your drive id' in parents"}).GetList()
		# We delete the file after 2 seconds because we don't need duplicate files in drive. In the mean time,
		# the picture is already extracted by the Word translating pc
                for file in fileList:
		    #This will print the content of that drive folder, we use to check what we have at this point of code
		    # It is for testing purposes, if we indeed deleted the file
                    print('Title: %s, ID: %s' % (file['title'], file['id']))
                    time.sleep(2)
                    drive.CreateFile({'id': file['id']}).Delete()
                time.sleep(2.5)
		#From here, we download the text file which contains the translated word 
                fileList = drive.ListFile({'q': " 'your drive id' in parents"}).GetList()

                for file in fileList:
                        print('Title: %s, ID: %s' % (file['title'], file['id']))
                        MSD = file['id']
		#We extract the data from the text file and return it to where we called this function
                try:
                    file_obj = drive.CreateFile({'id': MSD})
                    file_obj.GetContentFile('text.txt')
                    time.sleep(2)
                    f = open('text.txt', 'r')
                    file_contents = f.read()
                    print(file_contents)
                    return file_contents,3,1
		#in case it doesn't work we can try again	
                except:
                    return "Tekrar Deneyin",3,1
                    pass
           # This is in case we don't want to use the camera anymore, we can swing our finger to the IR sensor to switch tab   
            if (GPIO.input(R) == 0):
                cap.release()
                cv2.destroyAllWindows()
                B = 2
                K = 2
                time.sleep(0.1)
                return " ",0,2

# This is the function where we set the name of the weeks, since the datetime package gives the weekday in numbers (1-7)
# We put some spaces to make sure is displayed in the wanted place.
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
# The Final13.ppm is my star shaped logo that is in the same directory as this code's.
image = Image.open('Final3.ppm').convert('1')


# Alternatively load a different format image(png in this case), resize it, and convert to 1 bit color.
#image = Image.open('happycat.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')

# Display image.
disp.image(image)
disp.display()

# Make blank image for drawing. We use this to clear the screen.
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
draw.text((17,27),"Hosgeldiniz",font=font, fill=255) #Welcome message in Turkish to display
time.sleep(1.5)
disp.image(image)# We actually display it on the screen in here
disp.display()
time.sleep(1.5)

# This jprint function is just used to see the API(JSON) data in a more readable way,this is only on your python terminal, not toled screen
def jprint(obj):
	text = json.dumps(obj, sort_keys=True , indent=4)
	print(text)
# initial Weather and Currency Exchange data extraction from API
response = requests.get("Place your weather API link here for the weather of the city you want")
weather = response.json()
response = requests.get("Place your currency API link here, my link here is to give the Exchange Currency of Dollar")
currencyUSD = response.json()
response = requests.get("Place your currency API link here, my link here is to give the Exchange Currency of Euro")
currencyEUR = response.json()
response = requests.get("Place your currency API link here, my link here is to give the Exchange Currency of Pound")
currencyGBP = response.json()

#For the Weather info, we receive plenty of data but we are only interested in the following data:
#the city's name we want the weather of,
#The temperature
#The weather condition (Raining, cloudy etc.)
#The detailed weather Condition (Harsh Raining, Thick fog etc.)

city = str(weather['list'][0]['name']) # from the json data we retrive the name of the city
celcius = str(weather['list'][0]['main']['temp']) # from the json data we retrive the temperature in Celcius
basic = str(weather['list'][0]['weather'][0]['main']) # from the json data we retrive the weather condition
detail = str(weather['list'][0]['weather'][0]['description']) # from the json data we retrive the detailed weather condition

#We only take the 2 numbers after decimal point
USD = str(float('%.2f'% currencyUSD['rates']['TRY']))# Dollar - TL data
EUR = str(float('%.2f'% currencyEUR['rates']['TRY']))# Euro - TL data
GBP = str(float('%.2f'% currencyGBP['rates']['TRY'])) # Great Britain Pound - TL data

#This is to print in our Raspberry Pi python IDE terminal to see the data
print(city)
print(celcius)
print(basic)
print(detail)

print("1 USD = ",USD, "TRY")
print("1 EUR = ",EUR, "TRY")
print("1 GBP = ",GBP, "TRY")


count = 1 # This variable is just to initialize the loop's condition
A = 0 # This variable is used to switch between tabs
start_time = time.time()
#We start our infinite loop and repeat the data extraction process
while count == 1:
    
    current_time = time.time()
    elapsed_time = current_time - start_time
    # We extract data every 2 minutes.	
    if elapsed_time > 120:
        start_time = time.time()
        response = requests.get("Place your weather API link here for the weather of the city you want")
        weather = response.json()
        response = requests.get("Place your currency API link here, my link here is to give the Exchange Currency of Dollar")
        currencyUSD = response.json()
        response = requests.get("Place your currency API link here, my link here is to give the Exchange Currency of Euro")
        currencyEUR = response.json()
        response = requests.get("Place your currency API link here, my link here is to give the Exchange Currency of Pound")
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
	
	#We clear the screen after 2 mins to refresh it with new data
        draw.rectangle((0,0,width,height), outline=0, fill=0) 
        disp.image(image)
        disp.display()
        

    # We use this to change tabs
    if(GPIO.input(R) == 0):
        A = A + 1
        if(A == 4):
            A = 0
        time.sleep(0.1)

    

    # This is for the Data&Time display
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

    # This is for the Currency Exchange	display 
    if( A == 1 ):
        
        font = ImageFont.truetype('BMarmy.TTF', 12)
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((0,0),"1USD= " + USD + " TRY",font=font, fill=255)
        draw.text((0,15),"1EUR= " + EUR + " TRY",font=font, fill=255)
        draw.text((0,30),"1GBP= " + GBP+  " TRY",font=font, fill=255)

        disp.image(image)
        disp.display()
    # This is for the Weather info display 
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
    # This is for taking the picture of the word we want to translate
    if( A == 3 ):
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        disp.image(image)
        disp.display()
        C = 1
        while C==1:
                word = picture()
		#We print the translated word in the python IDE
                print(word)
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                disp.image(image)
                disp.display()
                try:
		    #We try to print on the TOLED the translated word
                    font = ImageFont.truetype('pixChicago.ttf', 10)
                    draw.text((0,25),word[0],font=font, fill=255)
                    disp.image(image)
                    disp.display()
                except:
                    pass
		# On the picture function, depending on how we want, we can either pass on the next tab by swinging our finger to the IR sensor
		# or continue translating 
                A = word[1]
                C = word[2]
                

                

        
                        
              
           
                
                

                        
                        
                  
                                
                
                
        
        
        
        



        

