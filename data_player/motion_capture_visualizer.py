import numpy as np
from matplotlib.animation import FuncAnimation
import utils


class MotionCaptureVisualizer(object):
    """
    Class which helps to visualize motion capture
    joints on video (matplotlib).

    :param fig: matplotlib figure
    :type fig: matplotlib.figure.Figure
    :param ax: matplotlib 2D axes
    :type ax: matplotlib.axes._subplots.AxesSubplot
    :param motion_capture: motion capture data
    :type motion_capture: MotionCapture
    :param video: video
    :type video: imageio.plugins.ffmpeg.FfmpegFormat.Reader
    :param camera: camera params
    :type camera: Camera
    """

    def __init__(self, fig, ax, motion_capture, video, camera):
        print(type(video))
        print(type(camera))
        self.fig = fig
        self.ax = ax
        self.image_points = utils.adapt_motion_data_for_video(
            motion_capture,
            camera
        )
        self.video = video
        self.camera = camera

    def update(self, frame):
        """
        Update the animation of the matplotlib figure.

        :param frame: frame number
        :type frame: int
        """
        self.ax.clear()
        image = self.video.get_data(frame)
        self.ax.imshow(image)

        image_points = self.image_points[frame]
        x_2d = image_points[:, 0]
        y_2d = image_points[:, 1]

        self.ax.scatter(x_2d, y_2d, marker='o', label='first', s=20., c='r')

    def get_animation(self, fps=30):
        """
        Get animation.

        :param fps: frames per second
        :type fps: int
        :return: matplotlib animation
        :rtype: matplotlib.animation.FuncAnimation
        """
        frames = np.arange(0, self.image_points.shape[0])
        interval = self.image_points.shape[0] / fps

        anim = FuncAnimation(
            self.fig,
            self.update,
            frames=frames,
            interval=interval,
            repeat=False,
        )
        return anim
