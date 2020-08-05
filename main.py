import argparse
import csv
import code.webscrape as ws

def main(args):
    path = args["path"]
    with open(path) as fh:
        rd = csv.DictReader(fh, delimiter=',')
        for row in rd:
            print(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path",
                        action="store",
                        help="file path to csv of players",
                        dest="path")
    args = vars(parser.parse_args())
    main(args)