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
    fps: int

    def get_joints_reduced_by_fps(self, fps) -> np.ndarray:
        """ Reduce motion capture frame rates.

        For example, every forth capture is if input is 30fps and a motion capture - 120fps.

        :param fps: reduce to fps
        :type fps: int
        :return: reduced motion capture data reduces fps, motion points, 3)
        :rtype: np.ndarray
        """
        diff = int(self.fps / fps)
        assert diff > 1, 'Difference should be at least 2 times bigger.'
        return self.joints[0::diff, :, :]
