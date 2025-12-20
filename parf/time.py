import time
# for i in range(101):
#     time.sleep(0.1)
#     print(f"\rПрогресс: {i}%", end=" ", flush=True)

for i in range(101):
    bar = "█" * (i//2) + " " *(50 - i//2)
    print(f"\r[{bar}] {i}%", end=" ", flush=True)
    time.sleep(1)