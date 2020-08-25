import argparse
import cv2
import numpy as np
import scipy.io as sio
import utils
from camera import Camera
from motion_capture import MotionCapture
from pose_visualizer import PoseVisualizer


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
                        help='Path to the motion capture file.',
                        default='../data/AMASS/F_amass_Subject_1.mat',
                        type=str)
    parser.add_argument('--movement_number',
                        help='Number of the AMASS subject movement (starting from 1).',
                        default=1,
                        type=int)
    parser.add_argument('--video_file',
                        help='Path to the video file.',
                        default='../data/PG1/F_PG1_Subject_1_L1.avi',
                        type=str)
    parser.add_argument('--output_video_file',
                        help='Path to the output video file (e.g., ../output/output.avi).',
                        type=str)
    return parser


def read_camera_params(extrinsic_data_path, camera_data_path):
    """Read camera's parameters.

    :param extrinsic_data_path: path of the extrinsic data
    :param camera_data_path: path of the camera's data
    :return: camera's params
    :rtype: Camera
    """
    extrinsic_data = np.load(extrinsic_data_path)
    rotation_matrix = extrinsic_data['rotationMatrix']
    translation_vector = extrinsic_data['translationVector']

    camera_data = np.load(camera_data_path)
    intrinsic_matrix = camera_data['IntrinsicMatrix']
    return Camera(rotation_matrix, translation_vector, intrinsic_matrix)


def read_motion_capture_data(motion_capture_data_path, movement_number):
    """Read motion capture data.

    :param motion_capture_data_path: path to the motion capture data
    :type motion_capture_data_path: str
    :param movement_number: number of the motion capture movement
    :type movement_number: int
    :return: motion capture data
    :rtype: np.ndarray
    """
    assert movement_number - 1 >= 0, 'Movement number has to start from 1.'

    motion_capture_data = sio.loadmat(motion_capture_data_path, simplify_cells=True)
    key = [key for key in motion_capture_data.keys() if key.startswith('Subject')][0]
    motion_capture_data = motion_capture_data[key]['move'][movement_number - 1]
    joints = motion_capture_data['jointsLocation_amass']
    skeleton = motion_capture_data['jointsParent']
    return MotionCapture(joints, skeleton)


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


def run_player(camera, motion_capture, video_file_path, **kwargs):
    """Run motion capture player.

    :param camera: camara params
    :type camera: Camera
    :param motion_capture: motion capture data
    :type motion_capture: MotionCapture
    :param video_file_path: path to the video file
    :type video_file_path: str
    :key output_video_file_path: path to the video file, optional
    """
    image_points = utils.adapt_motion_data_for_video(motion_capture.joints, camera)
    display_window(video_file_path, image_points)

    output_video_file_path = kwargs.get('output_video_file_path', None)
    if output_video_file_path:
        save_video(output_video_file_path, video_file_path, image_points)


def run_3d_player(motion_capture):
    """Show motion capture date in a 3d plot.

    :param motion_capture: motion capture data
    :type motion_capture: MotionCapture
    :return:
    """
    pose_visualizer = PoseVisualizer(motion_capture)
    pose_visualizer.show_plot()


if __name__ == '__main__':
    args = get_flags().parse_args()

    camera_params = read_camera_params(args.extrinsic_data, args.camera_data)
    motion_capture_data = read_motion_capture_data(args.motion_capture_data, args.movement_number)
    run_3d_player(motion_capture_data)
    run_player(
        camera_params,
        motion_capture_data,
        args.video_file,
        output_video_file_path=args.output_video_file
    )
