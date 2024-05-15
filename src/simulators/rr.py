import logging
import queue
from typing import List, Iterator, Optional

from src.consts import IDLE_TIME, SIMULATION_TIME
from src.request_utils import generate_new_request, Request, has_request_starved_at_queue

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

TIME_QUANTUM = 55.0  # ms [10, 100]


def simulate(
        max_queue_size: int,
        arrival_rate: float,
        simulation_time: float = SIMULATION_TIME
) -> List[Request]:
    requests_generator = generate_new_request(arrival_rate)
    results = _run_simulator(max_queue_size, requests_generator, simulation_time)
    # logger.info('RR Simulation Done')
    return results


def _run_simulator(max_queue_size: int, requests_generator: Iterator[Request], simulation_time: float) \
        -> List[Request]:
    q = queue.Queue(max_queue_size)
    all_requests = []

    current_time = 0
    incoming_request = next(requests_generator)  # First incoming request
    current_request: Optional[Request] = None

    while current_time < simulation_time:
        while incoming_request.arrival_time <= current_time:
            # generate artificial requests, and insert them to the queue
            # stop when the latest generated request is "in the future"
            try:
                q.put(incoming_request, block=False)
                incoming_request = next(requests_generator)
                all_requests.append(incoming_request)
            except queue.Full:
                # now the queue is full, so any of the other incoming request (up to the current time) is thrown
                # logger.debug('Queue is full')
                all_requests.append(incoming_request)
                while incoming_request.arrival_time <= current_time:
                    incoming_request = next(requests_generator)
                    all_requests.append(incoming_request)
                break

        if current_request and current_request.processing_time_leftover:
            # if the last processing wasn't finished and didn't starve
            # insert the unfinished request to the end of the queue
            # after inserting all new requests which got meanwhile
            try:
                q.put(current_request, block=False)
            except queue.Full:
                # if queue is full - pity, the request is thrown, although it hasn't finished
                pass

        if not q.empty():  # There are requests waiting to be handled
            # Round Robin algo, due to using PriorityQueue with processing_time as "key"
            current_request = q.get()
            if not has_request_starved_at_queue(current_request, current_time):
                # if the request waited for too long at the queue - just "throw" that request
                # otherwise - process it
                current_time += _handle_request(current_request, current_time)

        else:  # no incoming requests - server is "at rest"
            # logger.debug('Resting...')
            current_time += IDLE_TIME  # move the "clock"
    return all_requests


def _handle_request(request: Request, current_time: int) -> float:
    if not request.start_processing_time:  # if not already was in queue
        request.start_processing_time = current_time
        request.processing_time_leftover = request.processing_time

    burst_time = min(TIME_QUANTUM, request.processing_time_leftover)
    request.processing_time_leftover -= burst_time
    current_time += burst_time

    if request.processing_time_leftover == 0:  # if processing finished
        request.end_processing_time = current_time
        if current_time - request.arrival_time <= request.deadline:
            request.is_completed = True

    return burst_time  # return the processing time of that burst/quantum
