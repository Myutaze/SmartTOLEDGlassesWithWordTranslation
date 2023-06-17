# Convolutional Neural Network (a subtype of ANN)

# Importing the libraries
import time
import tensorflow as tf	 # tensorflow and keras are the main packages for this AI
from keras.preprocessing.image import ImageDataGenerator
import h5py #The Library responsible for saving trained data
from numpy import loadtxt
from keras.models import load_model
from imutils.object_detection import non_max_suppression
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


# We use ANN for the AI method, it is a topic on its own, so if you want learn more about it, you can find some courses 
# about deep learning and so on. But know that this method is processing heavy, the trade-off is that it is the one of the most
# (if not the most) accurate method out there when determining the outcome.

# Preprocessing the Training set
train_datagen = ImageDataGenerator(rescale = 1./255,    # We scale the images into a lower size to save cpu processing
                                   shear_range = 0.2,	# We do this for both the test and training sets
                                   zoom_range = 0.2,
                                   horizontal_flip = True)
training_set = train_datagen.flow_from_directory('dataset/training_set',
                                                 target_size = (256, 144),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

# Preprocessing the Test set
test_datagen = ImageDataGenerator(rescale = 1./255)
test_set = test_datagen.flow_from_directory('dataset/test_set',
                                            target_size = (256, 144),
                                            batch_size = 32,
                                            class_mode = 'categorical')

# Note that the below steps is only done once for training on the data because we won't be training it over and over
# everytime we run the code, it becomes time consuming. Instead we save the trained model and use it later.


# Initialising the CNN (a subtype of ANN)
#cnn = tf.keras.models.Sequential()

# Step 1 - Convolution
#cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=(256, 144, 3)))

# Step 2 - Pooling
#cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

# Adding a second convolutional layer
#cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
#cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

# Step 3 - Flattening
#cnn.add(tf.keras.layers.Flatten())

# Step 4 - Full Connection
#cnn.add(tf.keras.layers.Dense(units=128, activation='relu'))

# Step 5 - Output Layer
#cnn.add(tf.keras.layers.Dense(units=50, activation='softmax'))

# Compiling the CNN
#cnn.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['acc'])


# Training the CNN on the Training set and evaluating it on the Test set
#cnn.fit(x = training_set, validation_data = test_set, epochs = 4)

#cnn.save("cnn_model.h5") #Here we save the model after traininf the model is done.
#print("Saved cnn_modelrankup to disk")


cnn = load_model('cnn_model.h5') #Now we load the trained model
cnn.summary() #We print the summary of the model, to see what it is, its not necesary if you don't want to see it




# Making a single prediction



import numpy as np
from keras.preprocessing import image

import cv2
import shutil
from PIL import Image


net = cv2.dnn.readNet("frozen_east_text_detection.pb") # We use the text detection file here

a=0
b=0
c=1
d=0

# The text detection function:
def text_detector(image):
	#hasFrame, image = cap.read()
	orig = image
	(H, W) = image.shape[:2]

	(newW, newH) = (640, 320)
	rW = W / float(newW)
	rH = H / float(newH)

	image = cv2.resize(image, (newW, newH))
	(H, W) = image.shape[:2]

	layerNames = [
		"feature_fusion/Conv_7/Sigmoid",
		"feature_fusion/concat_3"]


	blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
		(123.68, 116.78, 103.94), swapRB=True, crop=False)

	net.setInput(blob)
	(scores, geometry) = net.forward(layerNames)

	(numRows, numCols) = scores.shape[2:4]
	rects = []
	confidences = []

	for y in range(0, numRows):

		scoresData = scores[0, 0, y]
		xData0 = geometry[0, 0, y]
		xData1 = geometry[0, 1, y]
		xData2 = geometry[0, 2, y]
		xData3 = geometry[0, 3, y]
		anglesData = geometry[0, 4, y]

		# loop over the number of columns
		for x in range(0, numCols):
			# if our score does not have sufficient probability, ignore it
			if scoresData[x] < 0.5:
				continue

			# compute the offset factor as our resulting feature maps will
			# be 4x smaller than the input image
			(offsetX, offsetY) = (x * 4.0, y * 4.0)

			# extract the rotation angle for the prediction and then
			# compute the sin and cosine
			angle = anglesData[x]
			cos = np.cos(angle)
			sin = np.sin(angle)

			# use the geometry volume to derive the width and height of
			# the bounding box
			h = xData0[x] + xData2[x]
			w = xData1[x] + xData3[x]

			# compute both the starting and ending (x, y)-coordinates for
			# the text prediction bounding box
			endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
			endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
			startX = int(endX - w)
			startY = int(endY - h)

			# add the bounding box coordinates and probability score to
			# our respective lists
			rects.append((startX, startY, endX, endY))
			confidences.append(scoresData[x])

	boxes = non_max_suppression(np.array(rects), probs=confidences)

	for (startX, startY, endX, endY) in boxes:

		startX = int(startX * rW)
		startY = int(startY * rH)
		endX = int(endX * rW)
		endY = int(endY * rH)

		# draw the bounding box on the image and crop it
		cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 3)
		cv2.imwrite("crop.jpg", orig)
		im = Image.open(r"crop.jpg")
		im1 = im.crop((startX , startY , endX, endY ))
		im2 = im1.save("pred.jpg")


# We prepare our Google drive to retrieve the picture taken by the Raspberry Pi
# That word on that picture will be used to translate it. Be sure to have the credentials.json(and setting.yaml if you are using it)
# in the same directory as this python code file.

gauth = GoogleAuth()

drive = GoogleDrive(gauth)

fileList = drive.ListFile({'q': " 'your drive id' in parents"}).GetList()
for file in fileList:
	print('Title: %s, ID: %s' % (file['title'], file['id']))
	drive.CreateFile({'id': file['id']}).Delete()

J = 0

while True:

	fileList = drive.ListFile({'q': " 'your drive id' in parents"}).GetList()
	#This will continously check if there is a file in drive and if there is, it will proceed to the if ( J == 1 ) part
	# to start predicting the word to translate
	for file in fileList:
		c = file['id']
		if(c!=d):
			print('Title: %s, ID: %s' % (file['title'], file['id']))
			d = file['id']
			J = 1
		MSD = file['id']
		try:
			file_obj = drive.CreateFile({'id': MSD})
			file_obj.GetContentFile('word.jpg')  # Download file as 'word.jpg'.
		except:
			pass
	if( J == 1 ):
	#Here is where we predict the word:
		try:
			pic = cv2.imread('word.jpg')
			array = pic  
			pic0 = cv2.resize(array, (640, 320), interpolation=cv2.INTER_AREA)
			text_detector(pic0)
			time.sleep(0.2)
			test_image = image.load_img('pred.jpg', target_size=(256, 144))
			test_image = image.img_to_array(test_image)
			test_image = np.expand_dims(test_image, axis=0)
			result = cnn.predict(test_image)
			#Then compare the predicted word and translate it
			if result[0][0] == 1:
				prediction = "All = Hepsi"

			elif result[0][1] == 1:
				prediction = "Always = Her Zaman"

			elif result[0][2] == 1:
				prediction = "Animal = Hayvan"

			elif result[0][3] == 1:
				prediction = "Book = Kitap"

			elif result[0][4] == 1:
				prediction = "Buy = Satin al"

			elif result[0][5] == 1:
				prediction = "Car = Araba"

			elif result[0][6] == 1:
				prediction = "Chair = Sandalye"

			elif result[0][7] == 1:
				prediction = "Child = Cocuk"

			elif result[0][8] == 1:
				prediction = "City = Sehir"

			elif result[0][9] == 1:
				prediction = "Day = Gun"

			elif result[0][10] == 1:
				prediction = "Drink = Icecek"

			elif result[0][11] == 1:
				prediction = "Family = Aile"

			elif result[0][12] == 1:
				prediction = "Food = Yemek"

			elif result[0][13] == 1:
				prediction = "Friend = Arkadas"

			elif result[0][14] == 1:
				prediction = "Home = Ev"

			elif result[0][15] == 1:
				prediction = "Inside = Iceride"

			elif result[0][16] == 1:
				prediction = "Laugh = Gulmek"

			elif result[0][17] == 1:
				prediction = "Less = Az"

			elif result[0][18] == 1:
				prediction = "Listen = Dinlemek"

			elif result[0][19] == 1:
				prediction = "Long = Uzun"

			elif result[0][20] == 1:
				prediction = "Man = Adam"

			elif result[0][21] == 1:
				prediction = "Month = Ay"

			elif result[0][22] == 1:
				prediction = "Name = Isim"

			elif result[0][23] == 1:
				prediction = "Never = Asla"

			elif result[0][24] == 1:
				prediction = "New = Yeni"

			elif result[0][25] == 1:
				prediction = "Noise = Gurultu"

			elif result[0][26] == 1:
				prediction = "Often = Siklikla"

			elif result[0][27] == 1:
				prediction = "Old = Eski"

			elif result[0][28] == 1:
				prediction = "Other = Diger"

			elif result[0][29] == 1:
				prediction = "Outside = Dişarida"

			elif result[0][30] == 1:
				prediction = "Pencil = Kalem"

			elif result[0][31] == 1:
				prediction = "People = Insanlar"

			elif result[0][32] == 1:
				prediction = "Power = Guc"

			elif result[0][33] == 1:
				prediction = "School = Okul"

			elif result[0][34] == 1:
				prediction = "Sell = Satmak"

			elif result[0][35] == 1:
				prediction = "Short = Kisa"

			elif result[0][36] == 1:
				prediction = "Silver = Gumus"

			elif result[0][37] == 1:
				prediction = "Sit = Oturmak"

			elif result[0][38] == 1:
				prediction = "Smile = Gulumsemek"

			elif result[0][39] == 1:
				prediction = "Sorry = Ozur dilemek"

			elif result[0][40] == 1:
				prediction = "Speak = Konusmak"

			elif result[0][41] == 1:
				prediction = "Study = Ders Calısmak"

			elif result[0][42] == 1:
				prediction = "Table = Masa"

			elif result[0][43] == 1:
				prediction = "Think = Dusunmek"

			elif result[0][44] == 1:
				prediction = "Time = Zaman"

			elif result[0][45] == 1:
				prediction = "Walk = Yurumek"

			elif result[0][46] == 1:
				prediction = "Water = Su"

			elif result[0][47] == 1:
				prediction = "Work = Calismak"

			elif result[0][48] == 1:
				prediction = "Write = Yazmak"

			elif result[0][49] == 1:
				prediction = "Year = Yil"

			else:
				prediction = "Unknown"
			#We print the translated word
			print(prediction)
			#Then write it on a text file and upload it to drive. 
			with open('translation.txt', 'w') as f:
				f.write(prediction)
			upload_text = 'translation.txt'
			gtext = drive.CreateFile({'parents': [{'id': 'your drive id'}]})
			gtext.SetContentFile(upload_text)
			gtext.Upload()
			print("Uploaded")
			fileList = drive.ListFile({'q': " 'your drive id' in parents"}).GetList()
			for file in fileList:
				print('Title: %s, ID: %s' % (file['title'], file['id']))
				time.sleep(5)
				drive.CreateFile({'id': file['id']}).Delete()


		except:
			pass
	
		J = 0














