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
