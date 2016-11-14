import argparse
import logging

from .tracker import Tracker

logging.basicConfig(level='DEBUG')

# TODO add runtime arguments to override the default configuration
# parser = argparse.ArgumentParser(description='Tracer: Drosophila tracker')
# parser.add_argument('video', type=str,
#                     help='video file path')
# args = parser.parse_args()

tracker = Tracker()
tracker.configure('config_sample_1.yml')
tracker.run()
