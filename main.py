from collections import defaultdict
from datetime import datetime

log_file = "sample.log"

# Constants
GET_ACTION = "GET"
HANDLE_ACTION = "HANDLE"

# Parse log file
server_response_times = defaultdict(list)
with open(log_file) as f:
    for line in f:
        split_line = line.split()
        date_str, guid, action, url, _, status, _, server_id = split_line
        if action == GET_ACTION:
            request_time = datetime.fromisoformat(date_str[:-4])
            server_response_times[server_id].append({"guid": guid, "time": request_time})
        elif action == HANDLE_ACTION:
            for req in server_response_times[server_id]:
                if req["guid"] == guid:
                    response_time = datetime.fromisoformat(date_str[:-4]) - req["time"]
                    server_response_times[server_id].append(response_time.total_seconds())
                    break

# Calculate average response times
avg_response_times = {}
for server_id, response_times in server_response_times.items():
    if response_times:  # Check if the list is not empty
        if isinstance(response_times[0], dict):
            # If response_times is a list of dictionaries, extract the 'time' values and use them to calculate the average
            time_values = [req['time'] for req in response_times]
            time_diffs = [(time_values[i + 1] - time_values[i]).total_seconds() for i in range(len(response_times) - 1)]
            avg_time_elapsed = sum(time_diffs) / len(time_diffs)
        else:
            # response_times is a list of floats, calculate the average directly
            avg_time_elapsed = sum(response_times) / len(response_times)

        avg_response_times[server_id] = avg_time_elapsed

# Identify slow servers
slow_servers = []
for server_id, avg_time in avg_response_times.items():
    if avg_time > 1:
        slow_servers.append(server_id)

print("Average Response Times:")
for server_id, avg_time in avg_response_times.items():
    print(f"Server {server_id}: {avg_time:.2f} seconds")

if slow_servers:
    print("Slow servers:")
    for server_id in slow_servers:
        print(server_id)
else:
    print("No slow servers found.")
