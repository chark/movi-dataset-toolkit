import argparse
import cv2
import imageio
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import utils
from camera import Camera
from matplotlib.animation import FuncAnimation
from motion_capture import MotionCapture
from motion_capture_visualizer import MotionCaptureVisualizer
from pose_3d_visualizer import Pose3DVisualizer


def get_flags():
    """Get command flags.

    :return: flags
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--extrinsic_data',
                        help='Path to the camera\'s extrinsic parameters.',
                        default='../data/Calib/Extrinsics_PG1.npz',
                        type=str)
    parser.add_argument('--camera_data',
                        help='Path to the camera\'s parameters file.',
                        default='../data/Calib/cameraParams_PG1.npz',
                        type=str)
    return parser


def main():
    pass


if __name__ == '__main__':
    main()
