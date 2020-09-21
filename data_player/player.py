# import sys
# sys.path.append("..")
import argparse
import cv2
import imageio
import numpy as np
import matplotlib.pyplot as plt
from common import utils
from common.camera import Camera
from common.motion_capture import MotionCapture
from matplotlib.animation import FuncAnimation
from data_player.visualizer.motion_capture_visualizer import MotionCaptureVisualizer
from data_player.visualizer.pose_3d_visualizer import Pose3DVisualizer


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
    parser.add_argument('--motion_capture_data',
                        help='Path to the motion capture file (.npz).',
                        default='../data/output/F_amass_Subject_1_1.npz',
                        type=str)
    parser.add_argument('--video_file',
                        help='Path to the video file.',
                        default='../data/output/F_PG1_Subject_1_L_1.avi',
                        type=str)
    parser.add_argument('--output_video_file',
                        help='Path to the output video file (e.g., ../output/output.avi).',
                        type=str)
    return parser


def display_window(video_file_path, image_points):
    """Display the player and run a video.

    :param video_file_path: path to the video file
    :type video_file_path: str
    :param image_points: points for painting
    :type image_points: np.ndarray
    """
    cap = cv2.VideoCapture(video_file_path)
    current_frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            frame_points = image_points[current_frame_num]
            for idx, val in enumerate(frame_points):
                frame = cv2.circle(
                    frame,
                    (val[0], val[1]),
                    radius=2,
                    color=(124, 252, 0),
                    lineType=cv2.LINE_AA,
                    thickness=-1
                )

            # Display the resulting frame
            cv2.imshow('Motion Capture', frame)

            current_frame_num = current_frame_num + 1

            # Close program by using key
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


def save_video(output_video_file_path, video_file_path, image_points):
    """Save results into a video file.

    :param output_video_file_path: path to the output video file
    :type output_video_file_path: str
    :param video_file_path: path to the video file
    :type video_file_path: str
    :param image_points: points for painting
    :type image_points: np.ndarray
    """
    cap = cv2.VideoCapture(video_file_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(output_video_file_path, fourcc, fps, (width, height))

    current_frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            frame_points = image_points[current_frame_num]
            for idx, val in enumerate(frame_points):
                frame = cv2.circle(
                    frame,
                    (val[0], val[1]),
                    radius=2,
                    color=(124, 252, 0),
                    lineType=cv2.LINE_AA,
                    thickness=-1
                )
            video.write(frame)
            current_frame_num = current_frame_num + 1
        else:
            break

    cap.release()
    video.release()


def run_opencv_player(camera, motion_capture, video_file_path, **kwargs):
    """Run motion capture player. Based on OpenCV.

    :param camera: camara params
    :type camera: Camera
    :param motion_capture: motion capture data
    :type motion_capture: MotionCapture
    :param video_file_path: path to the video file
    :type video_file_path: str
    :key output_video_file_path: path to the video file, optional
    """
    image_points = utils.adapt_motion_data_for_video(motion_capture, camera)
    display_window(video_file_path, image_points)

    output_video_file_path = kwargs.get('output_video_file_path', None)
    if output_video_file_path:
        save_video(output_video_file_path, video_file_path, image_points)


def run_3d_player(motion_capture, video_file_path, camera):
    """Show motion capture date in a 3d plot.

    :param motion_capture: motion capture data
    :type motion_capture: MotionCapture
    :param video_file_path: path to the video file
    :type video_file_path: str
    :param camera: camara params
    :type camera: Camera
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    video = imageio.get_reader(video_file_path, 'ffmpeg')
    motion_capture_visualizer = MotionCaptureVisualizer(fig, ax1, motion_capture, video, camera)

    ax2 = fig.add_subplot(2, 1, 2, projection='3d')
    pose_visualizer = Pose3DVisualizer(fig, ax2, motion_capture)

    fps = 30

    def update(frame):
        motion_capture_visualizer.update(frame)
        pose_visualizer.update(frame)

    frames = np.arange(0, motion_capture.get_joints_reduced_by_fps(fps).shape[0])
    interval = motion_capture.joints.shape[0] / fps

    anim = FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=interval,
        repeat=True,
    )
    plt.show(block=True)


if __name__ == '__main__':
    args = get_flags().parse_args()

    camera_params = utils.read_camera_params(args.extrinsic_data, args.camera_data)
    motion_capture_data = utils.read_motion_capture_data(args.motion_capture_data)
    run_3d_player(motion_capture_data, args.video_file, camera_params)
    run_opencv_player(
        camera_params,
        motion_capture_data,
        args.video_file,
        output_video_file_path=args.output_video_file
    )
