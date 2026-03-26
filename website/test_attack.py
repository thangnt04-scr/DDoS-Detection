"""Simulate attack traffic"""
import requests
import time
import threading

def send_requests(count, delay):
    for i in range(count):
        try:
            requests.get('http://localhost:5000/test', timeout=1)
        except:
            pass
        time.sleep(delay)

print("="*50)
print("Simulating DDoS Attack")
print("="*50)
print("Make sure detector is running and 'Start' clicked!")
print()

# Start multiple threads
threads = []
for i in range(10):
    t = threading.Thread(target=send_requests, args=(50, 0.05))
    t.start()
    threads.append(t)
    print(f"Thread {i+1} started")

print("\nAttack running... (will take ~3 seconds)")
print("Check detector: http://localhost:5000")

for t in threads:
    t.join()

print("\n✓ Attack completed!")
print("You should see ~500 packets with many marked as 'Attack'")
