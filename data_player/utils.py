import numpy as np


def convert_world_points_to_image_points(camera, world_points):
    """Convert world 3D points to image plane points.

    :param camera: camera's params
    :type camera: Camera
    :param world_points: World points (size, 3)
    :type world_points: np.ndarray
    :return: image plane points (size, 2)
    :rtype: np.ndarray of ints
    """
    translation_vector_expand = np.expand_dims(camera.translation_vector, axis=0)
    rot_tran_matrix = np.concatenate((camera.rotation_matrix, translation_vector_expand), axis=0)
    camera_matrix = np.dot(rot_tran_matrix, camera.intrinsic_matrix)
    image_points = np.zeros((world_points.shape[0], 2), dtype=int)

    for idx, val in enumerate(world_points):
        temp_matrix = np.append(val, 1)
        result = np.dot(temp_matrix, camera_matrix)
        u = result[0] / result[2]
        v = result[1] / result[2]
        image_points[idx, :] = [u, v]

    return image_points


def adapt_motion_data_for_video(motion_capture_data, camera):
    """Adapt motion capture (MoCap) data for the video.

    :param motion_capture_data: motion capture data (motion capture frames, motion points, 3)
    :param camera: camera's params
    :type camera: Camera
    :return: image plane points (video frames, motion points, 2)
    :rtype: np.ndarray
    """
    markers = reduce_motion_data_frame_rate(motion_capture_data)

    image_points = np.full((markers.shape[0], markers.shape[1], 2), 0, dtype=int)

    for i in range(0, markers.shape[1]):
        world_points = np.squeeze(markers[:, i, :])
        image_points[:, i] = convert_world_points_to_image_points(camera, world_points)

    return image_points


def reduce_motion_data_frame_rate(motion_capture_data):
    """ Reduce motion capture frame rates. Every forth capture is taken
    because a video is 30fps and a motion capture - 120fps.

    :param motion_capture_data: motion capture data (motion capture frames, motion points, 2)
    :type motion_capture_data: np.ndarray
    :return: reduced motion capture data (~motion capture frames/4, motion points, 3)
    :rtype: np.ndarray
    """
    markers = motion_capture_data[0::4, :, :]
    return markers
