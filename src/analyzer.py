from typing import List, Dict, Tuple

import matplotlib.pyplot as plt

from src.request_utils import Request, State


def success_percent(all_requests: List[Request]) -> float:
    """Calculate the success percent of requests."""
    total_requests = len(all_requests)
    if total_requests == 0:
        return 0
    successful_requests = sum(1 for req in all_requests if req.finish_state == State.FINISHED_SUCCESSFULLY)
    return successful_requests / total_requests * 100


def plot_success_percent(
        simulations: Dict[Tuple[float, int], List[Request]],
        queue_mechanism: str,
        time_quantum: int = None
) -> None:
    """Plot the success percent for varying parameters."""
    x_labels, percents = [], []
    for (arrival_rate, queue_size), requests in simulations.items():
        percent = success_percent(requests)
        x_labels.append(f"AR: {arrival_rate}, QS: {queue_size}")
        percents.append(percent)

    rr_title = f'TQ={time_quantum}' if time_quantum else ''

    plt.figure(figsize=(8, 6))
    plt.bar(x_labels, percents)
    plt.ylim(0, 100)
    plt.title(f'Success Percent for {queue_mechanism} {rr_title}')
    plt.xlabel('Parameters (Arrival Rate, Queue Size)')
    plt.ylabel('Success Percent')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def plot_success_percent_3d(
        simulations: Dict[Tuple[float, int], List[Request]],
        queue_mechanism: str,
        time_quantum: int = None
):
    """Plot the success percent for varying parameters in 3D."""
    arrival_rates, queue_sizes, success_percents = [], [], []

    for (arrival_rate, queue_size), requests in simulations.items():
        arrival_rates.append(arrival_rate)
        queue_sizes.append(queue_size)
        success_percents.append(success_percent(requests))

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(arrival_rates, queue_sizes, success_percents, c='r', marker='o')

    # Adding lines with different colors
    unique_arrival_rates = sorted(set(arrival_rates))
    color_map = plt.get_cmap('viridis', len(unique_arrival_rates))

    for i, arrival_rate in enumerate(unique_arrival_rates):
        indices = [j for j, ar in enumerate(arrival_rates) if ar == arrival_rate]
        xs = [arrival_rates[j] for j in indices]
        ys = [queue_sizes[j] for j in indices]
        zs = [success_percents[j] for j in indices]
        ax.plot(xs, ys, zs, color=color_map(i))

    rr_title = f'TQ={time_quantum}' if time_quantum else ''

    ax.set_xlabel('Arrival Rate')
    ax.set_ylabel('Queue Size')
    ax.set_zlabel('Success Percent')
    ax.set_title(f'Success Percent for {queue_mechanism} {rr_title}')

    plt.show()


def analyze_simulations(simulations: Dict[Tuple[float, int], List[Request]], queue_mechanism: str):
    """Perform a full analysis of the simulations."""
    # Plot success percent
    plot_success_percent(simulations, queue_mechanism)

    # Plot success percent in 3D
    plot_success_percent_3d(simulations, queue_mechanism)


def analyze_simulations_rr(
        simulations: Dict[Tuple[float, int], List[Request]],
        time_quantum: int,
        queue_mechanism: str
):
    """Perform a full analysis of the simulations."""
    # Plot success percent
    plot_success_percent(simulations, queue_mechanism, time_quantum)

    # Plot success percent in 3D
    plot_success_percent_3d(simulations, queue_mechanism, time_quantum)
