import logging
import queue
from typing import List, Iterator

from src.consts import IDLE_TIME, SIMULATION_TIME
from src.request_utils import generate_new_request, Request, has_request_starved_at_queue

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def simulate(
        max_queue_size: int,
        arrival_rate: float,
        simulation_time: float = SIMULATION_TIME
) -> List[Request]:
    requests_generator = generate_new_request(arrival_rate)
    results = _run_simulator(max_queue_size, requests_generator, simulation_time)
    # logger.info('FIFO Simulation Done')
    return results


def _run_simulator(
        max_queue_size: int,
        requests_generator: Iterator[Request],
        simulation_time: float
) -> List[Request]:
    q = queue.Queue(max_queue_size)
    all_requests = []

    current_time = 0
    incoming_request = next(requests_generator)  # First incoming request
    all_requests.append(incoming_request)

    while current_time < simulation_time:
        while incoming_request.arrival_time <= current_time:
            # generate artificial requests, and insert them to the queue
            # stop when the latest generated request is "in the future"
            try:
                q.put(incoming_request, block=False)
                incoming_request = next(requests_generator)
                if incoming_request.arrival_time <= simulation_time:
                    all_requests.append(incoming_request)
            except queue.Full:
                # now the queue is full, so any of the other incoming request (up to the current time) is thrown
                # logger.debug('Queue is full')
                if incoming_request.arrival_time <= simulation_time:
                    all_requests.append(incoming_request)
                while incoming_request.arrival_time <= current_time:
                    incoming_request = next(requests_generator)
                    if incoming_request.arrival_time <= simulation_time:
                        all_requests.append(incoming_request)
                break

        if not q.empty():  # There are requests waiting to be handled
            current_request = q.get()  # FIFO algorithm
            if not has_request_starved_at_queue(current_request, current_time):
                # if the request waited for too long at the queue - just "throw" that request
                # otherwise - process it
                _handle_request(current_request, current_time)
                current_time += current_request.processing_time
        else:  # no incoming requests - server is "at rest"
            # logger.debug('Resting...')
            current_time += IDLE_TIME  # move the "clock"
    return all_requests


def _handle_request(request: Request, current_time: int) -> None:
    request.start_processing_time = current_time

    current_time += request.processing_time  # processing simulation...
    request.end_processing_time = current_time

    if request.end_processing_time - request.arrival_time <= request.deadline:
        request.is_completed = True
