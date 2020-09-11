import argparse


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
                        default='./output-videos/',
                        type=str)
    return parser


def main():
    pass


if __name__ == '__main__':
    main()
