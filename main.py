import argparse
import yaml


def parse_args():
    parser = argparse.ArgumentParser(description='CSCI-576 Video Summarization')
    parser.add_argument('--data',
                        default='concert',
                        choices=['concert', 'meridian', 'soccer'],
                        help='concert, meridian, or soccer')
    return parser.parse_args()


def main():
    f = open("config.yaml")
    config = yaml.safe_load(f)
    args = parse_args()


    f.close()

if __name__ == '__main__':
    main()