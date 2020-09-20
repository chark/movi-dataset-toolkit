import argparse
import logging
import glob
from pathlib import Path
import cv2
import scipy.io as sio
import numpy as np

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)


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
    parser.add_argument('--v3d',
                        help='Path to the V3D folder.',
                        default='./V3D/',
                        type=str)
    parser.add_argument('--output',
                        help='Path to the the output of the prepared dataset..',
                        default='./output/',
                        type=str)
    return parser


def get_motions_list_from_v3d(v3d_file):
    """Get motions list from V3D files.

    :param v3d_file: V3D loaded file
    :type: dict
    :return: list of motions
    :rtype: numpy.ndarray
    """
    key = [key for key in v3d_file.keys() if key.startswith('Subject')][0]
    return v3d_file[key]['move']['motions_list']


def get_sub_video_ranges_from_v3d(v3d_file):
    """Get sub video ranges from V3D file.

    :param v3d_file: V3D loaded file
    :type: dict
    :return: sub video ranges [[start, end],...]
    :rtype: numpy.ndarray
    """
    key = [key for key in v3d_file.keys() if key.startswith('Subject')][0]
    return v3d_file[key]['move']['flags30']


def create_video_writer(width, height, fps, output_path):
    """Creates an object of the OpenCV video writer.

    :param width: width of the video
    :type width: int
    :param height: height of the video
    :type height: int
    :param fps: frame per second
    :type fps: float
    :param output_path: path to the output video
    :type output_path: str
    :return: OpenCV video writer
    :rtype: cv2.VideoWriter
    """
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    return cv2.VideoWriter(output_path, fourcc, fps, (width, height))


def split_video(video_path, v3d_path, output_path):
    """Split a video into sub videos.

    :param video_path: path of the video
    :type video_path: str
    :param v3d_path: path of the V3D file
    :type v3d_path: str
    :param output_path: path of output directory
    :type output_path: str
    """
    v3d_file = sio.loadmat(v3d_path, simplify_cells=True)
    motion_list = get_motions_list_from_v3d(v3d_file)
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

        video_start = video_ranges[current_video_num][0]
        video_end = video_ranges[current_video_num][1]

        if video_start <= current_frame_num <= video_end:
            if current_frame_num == video_start:
                output_video_name = Path(video_path).stem + '_' + str(current_video_num + 1) + '.avi'
                output_video_path = output_path + '/' + output_video_name
                video = create_video_writer(width, height, fps, output_video_path)

            video.write(frame)

            if current_frame_num == video_end:
                video.release()
                current_video_num = current_video_num + 1

        current_frame_num = current_frame_num + 1
    cap.release()


def split_videos(video_paths, v3d_paths, output_path):
    """Split videos into sub videos.

    :param video_paths: paths of videos
    :type video_paths: list of str
    :param v3d_paths: paths of V3D files
    :type v3d_paths: list of str
    :param output_path: path of the output directory
    :type output_path: str
    """
    logging.info('Starting splitting videos.')
    for video_path in video_paths:
        partial_name = video_path[15:-6]

        v3d_filtered_paths = list(filter(lambda element: partial_name in element, v3d_paths))
        if len(v3d_filtered_paths) > 0:
            logging.info('Splitting: ' + video_path)
            v3d_path = v3d_filtered_paths[0]
            split_video(video_path, v3d_path, output_path)
        else:
            logging.warning(video_path + ' couldn\'t be split: V3D file for the video is not found.')
    logging.info('Finished splitting videos.')


def split_amass_file(path, output_path):
    """Split an AMASS .mat file and save them into npz files.

    :param path: path of the Amass file
    :type path: str
    :param output_path: path of output directory
    :type output_path: str
    """
    amass_file = sio.loadmat(path, simplify_cells=True)
    key = [key for key in amass_file.keys() if key.startswith('Subject')][0]
    subject_id = amass_file[key]['id']
    subject = amass_file[key]['subject']
    moves = amass_file[key]['move']

    for idx, val in enumerate(moves):
        output_file_name = output_path + '/' + Path(path).stem + '_' + str(idx + 1) + '.npz'
        root_translation = val['RootTranslation_amass']
        joints_betas = val['jointsBetas_amass']
        joints_location = val['jointsLocation_amass']
        joints_exponential_mapping = val['jointsExpMaps_amass']
        joints_parent = val['jointsParent']
        description = val['description']
        np.savez(
            output_file_name,
            id=subject_id,
            subject=subject,
            root_translation=root_translation,
            joints_betas=joints_betas,
            joints_location=joints_location,
            joints_exponential_mapping=joints_exponential_mapping,
            joints_parent=joints_parent,
            description=description,
        )


def split_amass_files(amass_paths, output_path):
    """Split AMASS .mat files and save them into npz files.

    :param amass_paths: paths of Amass files
    :type amass_paths: list of str
    :param output_path: path of the output directory
    :type output_path: str
    """
    logging.info('Starting splitting Amass files.')
    for path in amass_paths:
        split_amass_file(path, output_path)

    logging.info('Finished splitting Amass files.')


if __name__ == '__main__':
    args = get_flags().parse_args()

    video_paths = glob.glob(args.videos + '/*.avi')
    v3d_paths = glob.glob(args.v3d + '/*.mat')
    amass_paths = glob.glob(args.amass + '/*.mat')
    output_path = args.output
    split_videos(video_paths, v3d_paths, output_path)
    split_amass_files(amass_paths, output_path)
