import itertools
from typing import List, Dict, Tuple

from tqdm import tqdm

from src.analyzer_3d import analyze_simulations
from src.consts import MAX_QUEUE_SIZES, ARRIVAL_RATES
from src.request_utils import Request
from src.simulators import rr, fifo, lifo


def _run_fifo_simulation() -> Dict[Tuple[float, int], List[Request]]:
    return {
        (arrival_rate, max_queue_size): fifo.simulate(max_queue_size, arrival_rate)
        for arrival_rate, max_queue_size in tqdm(list(itertools.product(ARRIVAL_RATES, MAX_QUEUE_SIZES)))
    }


def _run_lifo_simulation() -> Dict[Tuple[float, int], List[Request]]:
    return {
        (arrival_rate, max_queue_size): lifo.simulate(max_queue_size, arrival_rate)
        for arrival_rate, max_queue_size in tqdm(list(itertools.product(ARRIVAL_RATES, MAX_QUEUE_SIZES)))
    }


def _run_rr_simulation() -> Dict[Tuple[float, int, int], List[Request]]:
    return {
        (arrival_rate, max_queue_size, time_quantum): rr.simulate(max_queue_size, arrival_rate, time_quantum)
        for arrival_rate, max_queue_size, time_quantum in tqdm(list(itertools.product(ARRIVAL_RATES, MAX_QUEUE_SIZES)))
    }


def main():
    fifo_results = _run_fifo_simulation()
    analyze_simulations(fifo_results, 'FIFO')

    lifo_results = _run_lifo_simulation()
    analyze_simulations(lifo_results, 'LIFO')

    # rr_results = _run_rr_simulation()
    # analyze_simulations(rr_results, 'RoundRobin')


if __name__ == '__main__':
    main()
