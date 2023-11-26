import sys

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

print(f"Max concurrent instances: {n}")
print(f"Number of tank players: {t}")
print(f"Number of healer players: {h}")
print(f"Number of DPS players: {d}")
print(f"Minimum instance time: {t1}")
print(f"Maximum instance time: {t2}")
