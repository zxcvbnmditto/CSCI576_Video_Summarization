from Dataloader import Dataloader
from AlgorithmFactory import AlgorithmFactory
from VideoPlayer import VideoPlayer
# from VideoWriter import VideoWriter
import argparse
import glob
import yaml
import numpy as np

from tkinter import *

film_choice = ['concert', 'meridian', 'soccer', 'superbowl_2', 'steel', 'soccer_2', 'concert_2']
algo_choice = ['ShotAnalyzer', 'motionblock']

class Window(Tk):
    def __init__(self):
        super().__init__()

def parse_args():
    parser = argparse.ArgumentParser(description='CSCI-576 Video Summarization')
    parser.add_argument('--dataset',
                        default='concert',
                        choices=film_choice,
                        help=f'choose one from {film_choice}')
    parser.add_argument('--algorithm',
                        default=algo_choice[0],
                        choices=algo_choice,
                        help=f'choose one from {algo_choice}')
    parser.add_argument('--mask',
                        default='Off',
                        choices=['On', 'Off'],
                        help='Using On will play the result directly.')
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
    print('Data loaded -------------------')

    # Load existed masks or run algorithm to get one
    if args.mask=='Off':
        # Decide Algorithm to perform
        algo = AlgorithmFactory.create(args.algorithm, data)
        algo.run()
    else:
        data.mask = list(np.loadtxt(config['mask_path']+f'{args.dataset}_{args.algorithm}.txt'))

    # Summarize data
    data.summarize()

    # Play Video
    video_player = VideoPlayer(data, Tk())
    video_player.play()

    # Save mask
    if args.mask=='Off':
        np.savetxt(config['mask_path']+f'{args.dataset}_{args.algorithm}.txt', np.array(data.mask), fmt='%5i')
        # video writer
        # video_writer = VideoWriter(data)

if __name__ == '__main__':
    main()
