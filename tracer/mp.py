import argparse
import logging
import multiprocessing as mp
import os
import time

import imageio
import numpy as np

from . import tools


logging.basicConfig(
    level=logging.DEBUG,
    # level=logging.INFO,
    format='%(levelname)-8s %(asctime)s %(name)18s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


def get_image(reader, index):
    logger.debug("Reading frame %d", index)
    image = reader.get_data(index)
    image = image[:, :, 1]
    image.meta.index = index
    return image


def split_in_chunks(array, n=None):
    """Splits an array into `n` chunks."""
    n = n or mp.cpu_count()
    logger.info("Splitting video frames into %d chunks", n)
    chunks = np.array_split(array, n)
    for i, chunk in enumerate(chunks):
        logger.info(
            "Chunk %d contains frames in the range [%4d, %4d]",
            i+1, chunk[0], chunk[-1]
        )
    return chunks


def compute_background_model(filename, step):
    """Compute the background model of a video."""

    logger.info("Computing the background model")

    background_model = None
    distinct_frames = []
    bg = None
    bg_updated = None

    logger.debug("Reading frames in steps of %d frames", step)
    with imageio.get_reader(filename, format='FFMPEG') as reader:
        index = 0
        distinct_frames.append(get_image(reader, index))
        bg = distinct_frames[-1]

        while background_model is None and index < step * 100:
            index += step

            previous_image = distinct_frames[-1]
            image = get_image(reader, index)

            mse = tools.mean_squared_error(previous_image, image)
            logger.debug("MSE=%.1f", mse)
            if mse > 50:
                distinct_frames.append(image)
            else:
                continue

            bg_updated = np.median(
                np.dstack(distinct_frames), axis=2).astype(np.uint8)

            bg_mse = tools.mean_squared_error(bg, bg_updated)

            logger.debug(
                "Updating the background model using %d frames (MSE: %.1f)",
                len(distinct_frames), bg_mse
            )

            if bg_mse < 0.5:
                background_model = bg_updated
            else:
                bg = bg_updated

    return background_model


def process_video_chunk(filename, chunk):
    logger.info("Processing video chunk [%4d, %4d]", chunk[0], chunk[-1])
    time.sleep(2)


def main():
    parser = argparse.ArgumentParser(description='Background')
    parser.add_argument('filename', type=str,
                        help='video file path')
    args = parser.parse_args()

    logger.info("Video located in '%s'", args.filename)

    logger.info("Preparing the output folder")
    video_folder, video_filename = os.path.split(args.filename)
    video_name = os.path.splitext(args.filename)[0]
    output_folder = video_name
    if os.path.exists(output_folder):
        logger.info("Output folder already exists in '%s'", output_folder)
    else:
        os.mkdir(output_folder)
        logger.info("Output folder is '%s'", output_folder)

    logger.info("Reading video metadata...")
    with imageio.get_reader(args.filename, format='FFMPEG') as r:
        metadata = r.get_meta_data()
    for key, value in metadata.items():
        logger.info("\t%-14s %s", key, value)

    logger.info("Looking for an existing background model in output folder")
    background_filename = os.path.join(output_folder, "background.bmp")
    try:
        background_model = imageio.imread(background_filename)
    except OSError:
        logger.error("Background model not found in '%s", background_filename)
        background_model = compute_background_model(
            filename=args.filename,
            step=int(metadata['fps'])
        )
        logger.info("Saving background model as '%s'", background_filename)
        imageio.imwrite(
            background_filename, background_model, format='BMP')
    else:
        logger.info("Background model found '%s'", background_filename)

    frames = np.arange(metadata['nframes'])
    chunks = split_in_chunks(frames, 200)  # TOFIX using small chunks to test

    first_chunks = chunks[:20]  # TOFIX

    tasks = [(args.filename, chunk) for chunk in first_chunks]
    print(tasks)

    with mp.Pool(mp.cpu_count()) as pool:
        results = [pool.apply_async(process_video_chunk, t) for t in tasks]

    print(results)

    # processes = [
    #     mp.Process(target=process_video_chunk, args=(args.filename, chunk))
    #     for chunk in first_chunks
    # ]

    # for p in processes:
    #     p.start()

    # for p in processes:
    #     p.join()





    # q = mp.Queue()
    # read_process_1 = mp.Process(target=read, args=(args.filename, chunks[0], q))
    # read_process_2 = mp.Process(target=read, args=(args.filename, chunks[1], q))

    # read_process_1.start()
    # read_process_2.start()

    # read_process_1.join()
    # read_process_2.join()

    # frames_read = []
    # while q.qsize() != 0:
    #     frames_read.append(q.get())

    # q.close()

    # print(len(frames_read))

    # # Generate background model
    # with imageio.get_reader(args.filename, format='FFMPEG') as r:
    #     for i in frames[::metadata['fps']]:
    #         image = r.get_data(i)
    #         print(i, image.shape)

    # TODO

    logger.info("Completed")


if __name__ == '__main__':
    main()
