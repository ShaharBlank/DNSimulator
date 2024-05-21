"""
### Summary for Common Scenarios (in milliseconds)

Low Traffic Environment:
    Arrival Rate: 0.001 to 0.01 arrivals per millisecond (equivalent to 1 to 10 arrivals per second)
    Queue Size: 10 to 100 DNS queries

Medium Traffic Environment:
    Arrival Rate: 0.01 to 0.1 arrivals per millisecond (equivalent to 10 to 100 arrivals per second)
    Queue Size: 100 to 1000 DNS queries

High Traffic Environment:
    Arrival Rate: 0.1 to 1 arrival per millisecond (equivalent to over 100 arrivals per second)
    Queue Size: 1000 to 10,000 DNS queries

Extreme Traffic Environment:
    Arrival Rate: Exceeding 1 arrival per millisecond (equivalent to over 1,000 arrivals per second)
    Queue Size: 10,000 or more DNS queries
"""
ARRIVAL_RATES = [0.001, 0.005, 0.01, 0.05, 0.1, 0.25, 0.5, 1]  # average incoming requests per millisecond
MAX_QUEUE_SIZES = [10, 50, 100, 200, 500, 1000, 2000, 5000, 10000][::-1]
TIME_QUANTUMS = [10, 25, 50, 80, 100][::-1]

DEADLINE = 2000  # milliseconds == 2 secs
SIMULATION_TIME = 10000  # milliseconds == 10 secs
IDLE_TIME = 0.001  # milliseconds
