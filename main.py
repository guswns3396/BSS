import argparse
import csv
import code.webscrape as ws

def main(args):
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path",
                        action="store",
                        help="file path to csv of players",
                        dest="path")
    args = vars(parser.parse_args())
    main(args)