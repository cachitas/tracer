"""
My first attempt at using asyncio.

However this is not the same as parallelization...
This is useful when we need to wait for IO.
"""

import asyncio
from collections import deque
import logging
import sys

import imageio


logging.basicConfig(format='%(threadName)10s %(asctime)s %(name)18s: %(message)s')
logger = logging.getLogger('async')
# logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AsyncAllocator(object):
    def __init__(self, max_size):
        self._max_size = max_size
        self._allocated_size = 0
        self._waiting_allocations = deque()

    async def allocate_data(self, nbytes):
        if nbytes > self._max_size:
            raise Exception('Requested size exceeds total allowed allocation size')
        if not self.can_allocate_now(nbytes):
            logger.info(("Can't allocate %d bytes right now,"
                         " waiting for memory to be freed"), nbytes)
            future = asyncio.Future()
            self._waiting_allocations.append((future, nbytes))
            await future
        self._allocated_size += nbytes

    def deallocate_data(self, nbytes):
        self._allocated_size -= nbytes
        new_deque = deque()
        for ind, (future, size) in enumerate(self._waiting_allocations):
            if self.can_allocate_now(size):
                future.set_result(0)
            else:
                new_deque.append((future, size))
        self._waiting_allocations = new_deque

    def can_allocate_now(self, size):
        return self._allocated_size + size <= self._max_size


# filepath = 'sample_videos/single.avi'

# sem = asyncio.Semaphore(5000)
allocator = AsyncAllocator(2e9)


async def process_video(filename):
    tasks = list()
    frame_ind = 0

    with imageio.get_reader(filename, format='FFMPEG', mode='I') as reader:
        for frame in reader:
            # await sem.acquire()
            await allocator.allocate_data(frame.nbytes)

            task = asyncio.ensure_future(process_frame(frame, frame_ind))
            tasks.append(task)

            frame_ind += 1

            await asyncio.sleep(0)

    await asyncio.gather(*tasks)


async def process_frame(frame, frame_ind):
    logger.info("Processing frame {}".format(frame_ind))

    await asyncio.sleep(15.0)

    logger.info("Finished processing frame {}".format(frame_ind))

    # sem.release()
    allocator.deallocate_data(frame.nbytes)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_video(sys.argv[1]))
    logger.info("Completed")
    loop.close()


if __name__ == '__main__':
    main()
