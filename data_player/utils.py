import numpy as np


def convert_world_points_to_image_points(rotation_matrix, translation_vector, intrinsic_matrix, world_points):
    """Convert world 3D points to image plane points.

    :param rotation_matrix: camera's rotation matrix
    :param translation_vector: camera's translation vector
    :param intrinsic_matrix: camera's intrinsic matrix
    :param world_points: World points (size, 3)
    :type world_points: numpy array
    :return: image plane points (size, 2)
    :rtype: numpy array of ints
    """
    translation_vector_expand = np.expand_dims(translation_vector, axis=0)
    rot_tran_matrix = np.concatenate((rotation_matrix, translation_vector_expand), axis=0)
    camera_matrix = np.dot(rot_tran_matrix, intrinsic_matrix)
    image_points = np.zeros((world_points.shape[0], 2), dtype=int)

    for idx, val in enumerate(world_points):
        temp_matrix = np.append(val, 1)
        result = np.dot(temp_matrix, camera_matrix)
        u = result[0] / result[2]
        v = result[1] / result[2]
        image_points[idx, :] = [u, v]

    return image_points


def adapt_motion_data_for_video(motion_capture_data, rotation_matrix, translation_vector, intrinsic_matrix):
    """
    Adapt motion capture (MoCap) data for the video.

    :param motion_capture_data: motion capture data (motion capture frames, motion points, 2)
    :param rotation_matrix: camera's rotation matrix
    :param translation_vector: camera's translation vector
    :param intrinsic_matrix: camera's intrinsic matrix
    :return: image plane points (video frames, motion points, 2)
    :rtype: numpy array of ints
    """
    # Every forth capture is take because video is 30fps and motion capture 120fps.
    markers = motion_capture_data[0::4, :, :]

    image_points = np.full((markers.shape[0], markers.shape[1], 2), 0, dtype=int)

    for i in range(0, markers.shape[1]):
        world_points = np.squeeze(markers[:, i, :])
        image_points[:, i] = convert_world_points_to_image_points(
            rotation_matrix,
            translation_vector,
            intrinsic_matrix,
            world_points)

    return image_points
