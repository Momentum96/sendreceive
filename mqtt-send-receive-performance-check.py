from pprint import pprint
from datetime import datetime

with open("./receiver-lte.log", "r") as f:
    receive_lines = f.readlines()

receive_lines = [line for line in receive_lines if "payload" in line]

# pprint(receive_lines)
# print(len(receive_lines))

with open("./sender-lte.log", "r") as f:
    send_lines = f.readlines()

send_lines = [line for line in send_lines if "payload" in line]

# pprint(send_lines)
# print(len(send_lines))

time_diffs = []
date_format = "%Y-%m-%d %H:%M:%S,%f"

for s_line, r_line in zip(send_lines, receive_lines):
    s_t = datetime.strptime(s_line.split(" - ")[0], date_format)
    r_t = datetime.strptime(r_line.split(" - ")[0], date_format)
    print(f"send time : {s_t}")
    print(f"receive time : {r_t}")

    diff = r_t - s_t
    time_diffs.append(diff.total_seconds())

avg_diff = sum(time_diffs) / len(time_diffs)
max_diff = max(time_diffs)
min_diff = min(time_diffs)

print(f"Average time difference: {avg_diff:.6f} seconds")
print(f"Maximum time difference: {max_diff:.6f} seconds")
max_idx = time_diffs.index(max(time_diffs))
print(send_lines[max_idx])
print(receive_lines[max_idx])
print(f"Minimum time difference: {min_diff:.6f} seconds")
