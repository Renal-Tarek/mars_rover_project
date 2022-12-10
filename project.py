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
