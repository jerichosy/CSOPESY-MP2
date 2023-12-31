import logging
import random
import sys
import threading
import time
from queue import Queue

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# Ensure we have the correct amount of arguments (6 + the script name)
if len(sys.argv) != 7:
    print("Usage: python main.py <n> <t> <h> <d> <t1> <t2>")
    sys.exit(1)  # Exit the script with an error code

# Extract arguments and convert to the appropriate types
try:
    _, n, t, h, d, t1, t2 = sys.argv
    n = int(n)
    t = int(t)
    h = int(h)
    d = int(d)
    t1 = int(t1)
    t2 = int(t2)
except ValueError:  # Catch any conversion errors
    print("All arguments must be integers.")
    sys.exit(1)

# Synchronization variables
lock = threading.Lock()
tank_q = Queue(maxsize=t)
healer_q = Queue(maxsize=h)
dps_q = Queue(maxsize=d)

# Summary variables
instances_summary = [{'parties_served': 0, 'time_served': 0} for _ in range(n)]

def instance_manager(instance_id):
    while True:
        # logging.info('Waiting')
        lock.acquire()
        # Check if there are enough players of each role to form a party
        if not all([tank_q.qsize() >= 1, healer_q.qsize() >= 1, dps_q.qsize() >= 3]):
            lock.release()
            break  # Break the loop if we cannot form a standard party

        # Forming a party
        tank = tank_q.get()
        healer = healer_q.get()
        dps_list = [dps_q.get() for _ in range(3)]

        lock.release()

        # Run the instance (dungeon)
        logging.info(f"Instance {instance_id+1}: active")
        dungeon_time = random.randint(t1, t2)
        # print(f"Instance {instance_id}: running for {dungeon_time} seconds")  # debug
        time.sleep(dungeon_time)  # Simulates the time spent in the dungeon

        # Update summary information
        instances_summary[instance_id]['parties_served'] += 1
        instances_summary[instance_id]['time_served'] += dungeon_time

        # Instance becomes empty again
        logging.info(f"Instance {instance_id+1}: empty")

# Adding players to the queues
for _ in range(t):
    tank_q.put('Tank')
for _ in range(h):
    healer_q.put('Healer')
for _ in range(d):
    dps_q.put('DPS')

# Starting instance managers
instance_threads = [threading.Thread(target=instance_manager, args=(i,)) for i in range(n)]
for thread in instance_threads:
    thread.start()

# Wait for all instance threads to finish
for thread in instance_threads:
    # print(f"Waiting for {thread.name} to finish")
    thread.join()

# Printing summary
parties = 0
for i, summary in enumerate(instances_summary):
    print(f"Instance {i+1} served {summary['parties_served']} parties and was active for {summary['time_served']} seconds.")
    parties += summary['parties_served']
print(f"Total parties served: {parties}")
print("Leftovers:")
print(f"Tank: {tank_q.qsize()}/{t}")
print(f"Healer: {healer_q.qsize()}/{h}")
print(f"DPS: {dps_q.qsize()}/{d}")
