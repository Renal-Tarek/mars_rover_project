import numpy as np
import cv2



def color_thresh_obsticals(img, rgb_thresh=(160, 160, 160)):

    color_select = np.zeros_like(img[:,:,0])
    below_thresh = (img[:,:,0] < rgb_thresh[0]) \
                & (img[:,:,1] < rgb_thresh[1]) \
                & (img[:,:,2] < rgb_thresh[2]) \
                &(img[:,:,0] != 0) \
                &(img[:,:,1] != 0) \
                &(img[:,:,2] != 0)                
    color_select[below_thresh] = 1
    return color_select

def color_thresh_obsticals(img, rgb_thresh=(160, 160, 160)):

    color_select = np.zeros_like(img[:,:,0])
    below_thresh = (img[:,:,0] < rgb_thresh[0]) \
                & (img[:,:,1] < rgb_thresh[1]) \
                & (img[:,:,2] < rgb_thresh[2]) \
                &(img[:,:,0] != 0) \
                &(img[:,:,1] != 0) \
                &(img[:,:,2] != 0)                
    color_select[below_thresh] = 1
    return color_select

def color_thresh_rock(img):
    
    img1=img[:,:,::-1]
    hsv = cv2.cvtColor(img1, cv2.COLOR_RGB2HSV)

    #Define range of yellow colors in HSV
    lower_yellow = np.array([10, 100, 100],dtype='uint8')
    upper_yellow = np.array([255, 225 ,255],dtype='uint8')
    
    #Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #mask=cv2.bitwise_and(img,img,mask=out)
    return mask
