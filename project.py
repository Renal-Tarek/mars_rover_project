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

def rover_coords(binary_img):
    # Identify nonzero pixels
    ypos, xpos = binary_img.nonzero()
    # Calculate pixel positions with reference to the rover position being at the 
    # center bottom of the image.  
    x_pixel = -(ypos - binary_img.shape[0]).astype(np.float32)
    y_pixel = -(xpos - binary_img.shape[1]/2 ).astype(np.float32)
    return x_pixel, y_pixel

# Define a function to convert to radial coords in rover space
def to_polar_coords(x_pixel, y_pixel):
    # Convert (x_pixel, y_pixel) to (distance, angle) 
    # in polar coordinates in rover space
    # Calculate distance to each pixel
    dist = np.sqrt(x_pixel**2 + y_pixel**2)
    # Calculate angle away from vertical for each pixel
    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles

# Define a function to map rover space pixels to world space
def rotate_pix(xpix, ypix, yaw):
    # Convert yaw to radians
    yaw_rad = yaw * np.pi / 180
    xpix_rotated = (xpix * np.cos(yaw_rad)) - (ypix * np.sin(yaw_rad))
                            
    ypix_rotated = (xpix * np.sin(yaw_rad)) + (ypix * np.cos(yaw_rad))
    # Return the result  
    return xpix_rotated, ypix_rotated

def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale): 
    # Apply a scaling and a translation
    
    xpix_translated = ((xpix_rot / scale) + xpos)
    ypix_translated = ((ypix_rot / scale) + ypos)
    # Return the result  
    return xpix_translated, ypix_translated

def pix_to_world(xpix, ypix, xpos, ypos, yaw, world_size, scale):
    xpix_rot, ypix_rot = rotate_pix(xpix, ypix, yaw)
    xpix_tran, ypix_tran = translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale)
    x_pix_world = np.clip(np.int_(xpix_tran), 0, world_size - 1)
    y_pix_world = np.clip(np.int_(ypix_tran), 0, world_size - 1)
    return x_pix_world, y_pix_world

# Define a function to perform a perspective transform
def perspect_transform(img, src, dst):
           
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image
    
    return warped
# Apply the above functions in succession and update the Rover state accordingly
def perception_step(Rover):
    # Perform perception steps to update Rover()
    # TODO: 
    # NOTE: camera image is coming to you in Rover.img
    # 1) Define source and destination points for perspective transform
    img=Rover.img
    src=np.float32([[10,140],[300,140],[210,95],[120,95]])
    size=3
    buffer=10
    dst=np.float32([[img.shape[1]/2-size,img.shape[0]-buffer]
              ,[img.shape[1]/2+size,img.shape[0]-buffer],
             [img.shape[1] /2+ size, img.shape[0] - 2*size - buffer],
            [img.shape[1] /2- size, img.shape[0] - 2*size - buffer]])
     # 2) Apply perspective transform
    img=Rover.img
    img_transformed = perspect_transform(img, src, dst)

     # 3) Apply color threshold to identify navigable terrain/obstacles/rock samples
    img_terrain = color_thresh_road(img_transformed,rgb_thresh=(160, 160, 160))
    
    img_rock = color_thresh_rock(img_transformed)
                    
    img_obs = color_thresh_obsticals(img_transformed,rgb_thresh=(160, 160, 160))

     # 4) Update Rover.vision_image (this will be displayed on left side of screen)
    Rover.vision_image[:,:,0] = img_obs*255
    Rover.vision_image[:,:,1] = img_rock*255
    Rover.vision_image[:,:,2] = img_terrain*255

    # 5) Convert map image pixel values to rover-centric coords
    x_pix_road,y_pix_road=rover_coords(img_terrain)
    
    x_pix_rock,y_pix_rock=rover_coords(img_rock)
    
    x_pix_obs,y_pix_obs=rover_coords(img_obs)
    
    # 6) Convert rover-centric pixel values to world coordinates
    X_pos,Y_pos=Rover.pos
    Yaw=Rover.yaw
    scale=36
    
    x_pix_world_road ,y_pix_world_road=pix_to_world(x_pix_road, y_pix_road, X_pos, Y_pos, Yaw, 200, scale)
    
    x_pix_world_rock,y_pix_world_rock=pix_to_world(x_pix_rock,y_pix_rock, X_pos, Y_pos, Yaw, 200, scale)
    
    x_pix_world_obs,y_pix_world_obs=pix_to_world(x_pix_obs, y_pix_obs, X_pos, Y_pos, Yaw, 200, scale)
    
    # 7) Update Rover worldmap (to be displayed on right side of screen)
    Rover.worldmap[y_pix_world_obs,x_pix_world_obs, 0] += 1
    
    Rover.worldmap[y_pix_world_rock, x_pix_world_rock, 1] += 1
    
    Rover.worldmap[y_pix_world_road, x_pix_world_road, 2] += 1

 # 8) Convert rover-centric pixel positions to polar coordinates
    dist, angle=to_polar_coords(x_pix_road,y_pix_road)

     # Update Rover pixel distances and angles
    Rover.nav_dists = dist
    Rover.nav_angles = angle
    
 
    
    
    return Rover
