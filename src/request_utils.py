import random
from typing import Optional, Iterator

import numpy as np
from pydantic import BaseModel

from src.consts import DEADLINE


class Request(BaseModel):
    arrival_time: float
    processing_time: float

    deadline: float = DEADLINE
    start_processing_time: Optional[float] = None
    end_processing_time: Optional[float] = None
    is_completed: bool = False

    processing_time_leftover: Optional[float] = None  # in use only for RR


def generate_new_request(arrival_rate: float) -> Iterator[Request]:
    arrival_time = 0
    while True:
        # CACHE_T~N(0.0505, 0.012625), 0.001<=t=<0.1
        cache_search_time = np.random.normal(0.0505, 0.012625)
        # DISK_T~N(10,2.25) 1<=t=<20
        disk_search_time = np.random.normal(10, 2.25)
        # NETWORK_T~N(80,15) 20<=t=<140
        recursive_requests_time = np.random.normal(80, 15)

        is_in_cache = random.randint(1, 10) <= 7  # there's 70% chance of cache hit
        is_in_disk = random.randint(1, 10) <= 8  # there's 80% chance of disk hit, given that the request is not cached

        # always look for result in cache first
        processing_time = cache_search_time
        processing_time += disk_search_time if not is_in_cache else 0
        processing_time += recursive_requests_time if not is_in_cache and not is_in_disk else 0

        yield Request(
            arrival_time=arrival_time,
            processing_time=processing_time,
        )

        # Poisson's arrival times differences between 2 consecutive requests is actually X~Exp(1/𝜆)
        # X~P(𝜆) only gives the count, not the times
        arrival_time += np.random.exponential(1 / arrival_rate)


def has_request_starved_at_queue(request: Request, current_time: float) -> bool:
    # if the request was in queue for too long (more than it's deadline) - the queue "kicked it out"
    # before the server could process it
    request_waiting_time = current_time - request.arrival_time
    return request_waiting_time > request.deadline
