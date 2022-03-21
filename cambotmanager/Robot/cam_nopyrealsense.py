import os
import cv2


def take_images(snapshot_parent_inventory_item):
    cam = cv2.VideoCapture(3)
    name = snapshot_parent_inventory_item.base_directory + '/snapshot' \
           + str(len(snapshot_parent_inventory_item.snapshots)) + '.png'

    s, img = cam.read()
    if s:
        cv2.imwrite(name, img)

        size = os.path.getsize(name)
        return name, size
