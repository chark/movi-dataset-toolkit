from dataclasses import dataclass
import numpy as np


@dataclass
class Camera:
    """Camera's parameters"

    :param rotation_matrix: camera's rotation matrix
    :type rotation_matrix: np.ndarray
    :param translation_vector: camera's translation vector
    :type translation_vector: np.ndarray
    :param intrinsic_matrix: camera's intrinsic matrix
    :type intrinsic_matrix: np.ndarray
    """
    rotation_matrix: np.ndarray
    translation_vector: np.ndarray
    intrinsic_matrix: np.ndarray
