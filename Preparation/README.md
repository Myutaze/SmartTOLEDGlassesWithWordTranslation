# The Logic

So it's important to note with what kind of logic we are working here. 

The Weather and Currency Exchange data will be taken over the internet and directly printed on the display, no problem there.

But for Word Translation, we will take a picture of a word from the camera and send it to the main PC who will translate the word and return the translated data back to Raspberry Pi. For that we will use Google Drive. We will send our picture to our Google Drive from Raspberry Pi then delete it after the picture was extracted by the main PC (because in drive when you upload a file with the same name, the new file gets an iterated name like New Folder(1)) then our main PC will translate the word, save it as a text file then send it back to the same drive which it will get deleted after the Raspberry Pi will extract it from drive. Then it will display it on the Toled Screen. We are using the Google drive API so i suggest you watch this video first to build your Google drive API as there is some preparation to do before implementing to python:

https://www.youtube.com/watch?v=2mnKE9IERt4

You can also search for something called settings.yaml file in case you don't want to authenticate each time you run the code, i will be using that. The way i do it is a little diffrent than the video because we are going to place our picture in a specific folder rather than to the root of drive but it is not complicated, you should be able to follow.

# Weather and Currency Exchange API
