import logging
import multiprocessing
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)18s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger('copulation_detector')


def process_video(video):
    queue = multiprocessing.Queue(3)
    queue.put(3)
    queue.put(3)
    queue.put(3)
    queue.put(3)

    logger.info(queue)


def main():
    process_video(sys.argv[1])
    logger.info("Completed")


if __name__ == '__main__':
    main()
