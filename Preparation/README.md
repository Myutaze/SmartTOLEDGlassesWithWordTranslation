# The Logic

So it's important to note with what kind of logic we are working here. 

The Weather and Currency Exchange data will be taken over the internet and directly printed on the display, no problem there.

But for Word Translation, we will take a picture of a word from the camera (the camera screen will be on the Raspberry Pi monitor) and send it to the main PC who will determine/predict the word in English and translate the word and return the translated data back to Raspberry Pi. For that we will use Google Drive. We will send our picture to our Google Drive from Raspberry Pi then delete it after the picture was extracted by the main PC (because in drive when you upload a file with the same name, the new file gets an iterated name like New Folder(1)) then our main PC will translate the word, save it as a text file then send it back to the same drive which it will get deleted after the Raspberry Pi will extract it from drive. Then it will display it on the Toled Screen. We are using the Google drive API so i suggest you watch this video first to build your Google drive API as there is some preparation to do before implementing to python:

https://www.youtube.com/watch?v=2mnKE9IERt4

You can also search for something called settings.yaml file along with credentials.json in case you don't want to authenticate each time you run the code, i will be using that. The way i do it is a little diffrent than the video because we are going to place our picture in a specific folder rather than to the root of drive, it isn't difficult to understand. If you don't understand a line of code, internet is your friend. Don't forget to put your client_secret.json (and if you are using it, the settings.yaml and credentials.json files too) in the same directory as your python code in the main PC.

For word translation on the main PC we will also need a text detection. For this we use EAST Detector for Text Detection (https://github.com/ZER-0-NE/EAST-Detector-for-text-detection-using-OpenCV). You can download the frozen_east_text_detection.pb from there, we will be using that file for word detection. Keep that file in the same directory as your python code for word translation on the main PC. What this will enable is that we can detect the text and crop it to that selection so that we have better chance of predicting the correct word its written on it. For Example:

 - The picture we took from Raspberry Pi:


<img src = "https://github.com/Myutaze/SmartTOLEDGlassesWithWordTranslation/assets/123553691/f7c428c0-2db3-4bc4-afd7-d5c67d0ba29d" width = "300" >

<br>
<br>

- The cropped image after sending the image to the main PC:


<img src = "https://github.com/Myutaze/SmartTOLEDGlassesWithWordTranslation/assets/123553691/aee06e04-6ae4-424e-a49c-56730708901f" width = "300" >

<br>
<br>


For the 50 words, i opened up a powerpoint presentation for each word and copy-pasted 720 times the same word on each page then i changed each of their font. I would have provided the RAR file containing it but Github doesn't accept big files, you can choose the words you want and do the same method as me. You open a powerpoint, on the first slide write any word you want, make it big like 72 or 48 size font. Then duplicate slide until you have 720 total, now the grindy part: visit each slide and change the word's font. You will do this once but save it because it will be reused for the other words. After that you can export all slides as png into a folder named after the word you want to translate (so if the word you want to translate is "Time" then when exporting the slides as png export it in a folder called "Time"). This is for 1 word, now you can do for the rest, all you have to do is, on the powerpoint use the find and replace tool and change the word then repeat the process of exportation.

Now in the folder where you will run the python code, make a folders as the following:

- dataset:
  - test_set
  - training_set
        
So inside the dataset folder you have 3 more folders. In the test_set and training_set put all your 50 word folders. These folders will be used as training and test for the AI.

# Weather and Currency Exchange API

Weather and Currency Exchange info from the internet through API. The 2 websites i used for this are:

- Openweathermap.com

- freecurrencyapi.net (which became currencyapi.com)

You don't have to choose those 2 websites you can choose any provider. You will need to read the documentation of those providers on how to get the API links or keys. Usually they explain it on their domain on to how to implement it.


