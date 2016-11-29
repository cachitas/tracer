import argparse
import logging
import sys

from .tracker import Tracker

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-18s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='tracer.log',
                    filemode='w')

console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-18s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


# TODO add runtime arguments to override the default configuration
parser = argparse.ArgumentParser(description='Tracer: Drosophila tracker')
parser.add_argument('video_filepath', type=str,
                    help='video file path')
parser.add_argument('number_of_flies', type=int,
                    help='number of flies in roi')
parser.add_argument('-a', '--area', type=int, default=500,
                    help='minimum area for a valid blob (px)')
args = parser.parse_args()

tracker = Tracker()
# tracker.configure('config_sample_1.yml')
tracker.configure(**vars(args))
tracker.run()
