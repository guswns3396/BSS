import argparse
import code.webscrape as ws

def main(args):
    # if gather data chosen
    if args['years']:
        ws.extractTrainingSet(args['years'][0], args['years'][1], args['filename'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run BSS')
    group = parser.add_mutually_exclusive_group(required=True)
    # gather data
    group.add_argument('-g', '--gather',
                       action='store',
                       type=int,
                       nargs=2,
                       metavar='YEAR',
                       dest='years',
                       help='Gather data from start_year to end_year')
    parser.add_argument('-o', '--output',
                        action='store',
                        metavar='FILENAME',
                        default='training_set.csv',
                        dest='filename',
                        help='Name of file to output after gathering data')

    group.add_argument('-t', '--train', help='Train model')
    group.add_argument('-i', '--inference', help='Run inference')

    args = vars(parser.parse_args())
    main(args)
