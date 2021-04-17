from Dataloader import Dataloader
from AlgorithmFactory import AlgorithmFactory
import argparse
import glob
import yaml



def parse_args():
    parser = argparse.ArgumentParser(description='CSCI-576 Video Summarization')
    parser.add_argument('--dataset',
                        default='concert',
                        choices=['concert', 'meridian', 'soccer'],
                        help='concert, meridian, or soccer')
    parser.add_argument('--algorithm',
                        default='motionblock',
                        choices=['motionblock'],
                        help='motionblock')
    return parser.parse_args()


def main():
    # Config => Constants
    f = open("config.yaml")
    config = yaml.safe_load(f)
    f.close()
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



if __name__ == '__main__':
    main()