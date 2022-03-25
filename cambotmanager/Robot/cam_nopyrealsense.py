import os
import cv2
from PIL.Image import Image
from datetime import datetime


def take_images(snapshot_parent_inventory_item):
    cam = cv2.VideoCapture(3)
    path = snapshot_parent_inventory_item.base_directory + '/' + snapshot_parent_inventory_item.image_directory + '/'
    name = 'snapshot_RGB_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    whole_path = path + name
    s, img = cam.read()
    if s:
        cv2.imwrite(whole_path, img)
        return whole_path
