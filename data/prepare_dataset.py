import argparse
import cv2
import scipy.io as sio
from pathlib import Path


def get_flags():
    """Get command flags.

    :return: flags
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--amass',
                        help='Path to the AMASS folder.',
                        default='./AMASS/',
                        type=str)
    parser.add_argument('--videos',
                        help='Path to the video folder.',
                        default='./Videos/',
                        type=str)
    parser.add_argument('--output_videos',
                        help='Path to the the output of split video folder.',
                        default='./output_videos/',
                        type=str)
    return parser


def get_motion_list_from_v3d(v3d_file):
    key = [key for key in v3d_file.keys() if key.startswith('Subject')][0]
    return v3d_file[key]['move']['motions_list']


def get_sub_video_ranges_from_v3d(v3d_file):
    key = [key for key in v3d_file.keys() if key.startswith('Subject')][0]
    return v3d_file[key]['move']['flags30']


def create_video_writer(width, height, fps, output_path):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    return cv2.VideoWriter(output_path, fourcc, fps, (width, height))


def split_video(video_path, v3d_path, output_path):
    v3d_file = sio.loadmat(v3d_path, simplify_cells=True)
    motion_list = get_motion_list_from_v3d(v3d_file)
    motions_num = len(motion_list)
    video_ranges = get_sub_video_ranges_from_v3d(v3d_file)

    cap = cv2.VideoCapture(video_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    current_frame_num = 1
    current_video_num = 0

    video = None
    while cap.isOpened():
        if current_video_num >= motions_num:
            break

        ret, frame = cap.read()

        video_start = video_ranges[current_video_num, 0]
        video_end = video_ranges[current_video_num, 1]

        if video_start <= current_frame_num <= video_end:
            if current_frame_num == video_start:
                output_video_name = Path(video_path).stem + "_" + str(current_video_num + 1) + ".avi"
                output_video_path = output_path + "/" + output_video_name
                video = create_video_writer(width, height, fps, output_video_path)

            video.write(frame)

            if current_frame_num == video_end:
                video.release()
                current_video_num = current_video_num + 1

        current_frame_num = current_frame_num + 1
    cap.release()


def main():
    video_path = "./Videos/F_PG1_Subject_1_L.avi"
    v3d_path = "./V3D/F_v3d_Subject_1.mat"
    output_path = "./output_videos/"
    split_video(video_path, v3d_path, output_path)


if __name__ == '__main__':
    main()
