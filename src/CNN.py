import tensorflow as tf
from tensorflow import keras
import cv2 
import numpy as np 
from PIL import Image
import pyautogui 
model = tf.keras.models.load_model('..//Assets/my_model.h5')
cap=cv2.VideoCapture(0)
while True:
        _, frame = cap.read()

        #Convert the captured frame into RGB
        im = Image.fromarray(frame, 'RGB')

        #Resizing into 100x100 because we trained the model with this image size.
        im = im.resize((100,100))
        img_array = np.array(im)

        #Our keras model used a 4D tensor, (images x height x width x channel)
        #So changing dimension 128x128x3 into 1x128x128x3 
        img_array = np.expand_dims(img_array, axis=0)

        #Calling the predict method on model to predict 'me' on the image
        prediction = model.predict(img_array)

        #if prediction is 0, which means I am missing on the image, then show the frame in gray color.
        index= np.argmax(prediction)
        if(index==0):
            print("Up")
            pyautogui.press('up')
        if(index==1):
            print("Right")
            pyautogui.press('Right')
        if(index==2):
            print("Down")
            pyautogui.press('Down')
        if(index==3):
            print("Left")
            pyautogui.press('Left')
        cv2.imshow("Capturing", frame)
        key=cv2.waitKey(1)
        if key == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()
