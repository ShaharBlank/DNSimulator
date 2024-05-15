"""
### Summary for Common Scenarios (in milliseconds)

- High-Traffic Public DNS Resolver: 
  - Arrival Rate: 10,000 queries per second (1 request every 0.1 milliseconds).
  - Queue Size: 10,000 to 50,000 requests.
  
- Moderate-Traffic ISP/Enterprise DNS Server:
  - Arrival Rate: 1,000 to 5,000 queries per second (1 request every 1 to 0.2 milliseconds).
  - Queue Size: 1,000 to 5,000 requests.
  
- Popular Domain Authoritative DNS Server:
  - Arrival Rate: 500 to 2,000 queries per second (1 request every 2 to 0.5 milliseconds).
  - Queue Size: 1,000 to 5,000 requests.
  
- Smaller Authoritative DNS Server:
  - Arrival Rate: 10 to 100 queries per second (1 request every 100 to 10 milliseconds).
  - Queue Size: 100 to 500 requests.
"""
ARRIVAL_RATES = [0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]  # average incoming requests per millisecond
MAX_QUEUE_SIZES = [200, 500, 1000, 2000, 5000, 8000, 10000][::-1]
TIME_QUANTUMS = [5, 10, 25, 50, 80, 100, 200][::-1]

DEADLINE = 2000  # milliseconds == 2 secs
SIMULATION_TIME = 10000  # milliseconds == 10 secs
IDLE_TIME = 0.001  # milliseconds
