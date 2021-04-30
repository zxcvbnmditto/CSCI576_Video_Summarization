from Dataloader import Dataloader
from AlgorithmFactory import AlgorithmFactory
from VideoPlayer import VideoPlayer
import argparse
import glob
import yaml
from videoWriter import VideoWriter
from videoGUI import videoGUI
from tkinter import *

class Window(Tk):
    def __init__(self):
        super().__init__()


def parse_args():
    parser = argparse.ArgumentParser(description='CSCI-576 Video Summarization')
    parser.add_argument('--dataset',
                        default='meridian',
                        choices=['concert', 'meridian', 'soccer'],
                        help='concert, meridian, or soccer')
    parser.add_argument('--algorithm',
                        default='motionblock',
                        choices=['motionblock'],
                        help='AlgorithmDemo')
    return parser.parse_args()


def main():
    # Config => Constants
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    # Arguments
    args = parse_args()

    # Dataloader
    data = Dataloader(config["video_path"] + args.dataset,
                      config["audio_path"] + args.dataset + ".wav",
                      config["fps"],
                      config["width"],
                      config["height"])

    # Decide Algorithm to perform
    algo = AlgorithmFactory.create(args.algorithm, data)
    algo.run()

    # Summarize data
    data.summarize()

    #video writer
    video_writer = VideoWriter(data)

    # PLay Video
    video_GUI = videoGUI(Tk(), 'new_window')
    # video_player.play()


if __name__ == '__main__':
    main()