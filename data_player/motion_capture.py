from dataclasses import dataclass
import numpy as np


@dataclass
class MotionCapture:
    """Camera's parameters"

    :param joints: locations of joints
    :type joints: np.ndarray
    :param skeleton: skeleton (synonym jointsParent)
    :type skeleton: np.ndarray
    """
    joints: np.ndarray
    skeleton: np.ndarray
