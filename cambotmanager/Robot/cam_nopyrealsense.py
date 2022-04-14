import time
import cv2
from datetime import datetime


# this takes pictures with the OpenCV library
def take_images(snapshot_parent_inventory_item):
    cam_port = 5  # the Camera with shel be used if images look strange swap number start with 0
    cam = cv2.VideoCapture(cam_port)
    path = snapshot_parent_inventory_item.base_directory + '/' + snapshot_parent_inventory_item.image_directory + '/'
    name = 'snapshot_RGB_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    whole_path = path + name
    s, img = cam.read()
    if s:
        cv2.imwrite(whole_path, img)
        return whole_path
