import os

import pyrealsense2 as rs
import numpy as np
import cv2
from PIL import Image


def take_images(snapshot_parent_inventory_item):
    color_name = snapshot_parent_inventory_item.base_directory + '/color_snapshot' \
                 + str(len(snapshot_parent_inventory_item.snapshots)) + '.png'
    depth_name = snapshot_parent_inventory_item.base_directory + '/depth_snapshot' \
                 + str(len(snapshot_parent_inventory_item.snapshots)) + '.png'

    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()

    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break
    if not found_rgb:
        print("The demo requires Depth camera with Color sensor")
        exit(0)

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    if device_product_line == 'L500':
        config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
    else:
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)

    try:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Save images
        col_img = Image.fromarray(color_image)
        dep_img = Image.fromarray(depth_image)
        col_img.save(color_name)
        dep_img.save(depth_name)
        cv2.waitKey(1)

    finally:

        # Stop streaming
        pipeline.stop()
        size = os.path.getsize(color_name) + os.path.getsize(depth_name)
        return color_name, depth_name, size
