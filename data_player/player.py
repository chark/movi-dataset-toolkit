import argparse
import cv2
import numpy as np
import scipy.io as sio
import utils


def display_window(video_file_path, points):
    cap = cv2.VideoCapture(video_file_path)
    current_frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            frame_points = points[current_frame_num]
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


def run_player(extrinsic_data_path, camera_data_path, motion_capture_data_path, movement_number, video_file_path):
    extrinsic_data = np.load(extrinsic_data_path, )
    rotation_matrix = extrinsic_data['rotationMatrix']
    translation_vector = extrinsic_data['translationVector']

    camera_data = np.load(camera_data_path)
    intrinsic_matrix = camera_data['IntrinsicMatrix']

    assert movement_number - 1 >= 0, 'Movement number has to start from 1.'

    motion_capture_data = \
        sio.loadmat(motion_capture_data_path, simplify_cells=True)['Subject_1_F_amass']['move']
    joints = motion_capture_data[movement_number - 1]['jointsLocation_amass']

    points = utils.adapt_motion_data_for_video(joints, rotation_matrix, translation_vector, intrinsic_matrix)
    display_window(video_file_path, points)


if __name__ == '__main__':
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
    args = parser.parse_args()

    run_player(
        args.extrinsic_data,
        args.camera_data,
        args.motion_capture_data,
        args.movement_number,
        args.video_file
    )
