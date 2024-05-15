import itertools
from typing import Callable, List

from src.consts import MAX_QUEUE_SIZES, ARRIVAL_RATES, TIME_QUANTUMS
from src.request_utils import Request
from src.simulators import rr, fifo, lifo


def _run_simulation(simulator: Callable[[int, float], List[Request]]) -> None:
    algorithm_name = str(simulator.__module__).split('.')[-1].upper()
    print(f'{algorithm_name} Simulation:')

    for arrival_rate, max_queue_size in itertools.product(ARRIVAL_RATES, MAX_QUEUE_SIZES):
        results = simulator(max_queue_size, arrival_rate)
        success_ratio = round(len([r for r in results if r.is_completed]) / len(results) * 100, 2)
        print(f'arrival_rate={arrival_rate}, max_queue_size={max_queue_size}: {success_ratio}%')

    print('-----------------------------------------')


def _run_rr_simulation() -> None:
    print(f'RR Simulation:')

    for arrival_rate, max_queue_size, time_quantum in itertools.product(ARRIVAL_RATES, MAX_QUEUE_SIZES, TIME_QUANTUMS):
        results = rr.simulate(max_queue_size, arrival_rate, time_quantum)
        success_ratio = round(len([r for r in results if r.is_completed]) / len(results) * 100, 2)
        print(f'arrival_rate={arrival_rate}, '
              f'max_queue_size={max_queue_size}, '
              f'time_quantum={time_quantum}: '
              f'{success_ratio}%')

    print('-----------------------------------------')


def main():
    _run_simulation(fifo.simulate)
    _run_simulation(lifo.simulate)
    _run_rr_simulation()


if __name__ == '__main__':
    main()
