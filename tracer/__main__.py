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
# parser = argparse.ArgumentParser(description='Tracer: Drosophila tracker')
# parser.add_argument('video', type=str,
#                     help='video file path')
# args = parser.parse_args()

tracker = Tracker()
tracker.configure('config_sample_1.yml')
tracker.run()
