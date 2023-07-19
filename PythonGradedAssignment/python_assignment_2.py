import psutil

# Checking CPU Usage
def cpu_usage(threshold):
    print("Monitoring CPU usage")
    while True:
        try:
            cpu_usage = psutil.cpu_percent()
            if cpu_usage > threshold:
                print(f"Alert! CPU usage exceeds threshold: {cpu_usage}%")

        except Exception as ex:
            print(f"An error occurred while monitoring CPU usage: {str(ex)}")

# Threshold Value
threshold = 80

try:
    cpu_usage(threshold)
except KeyboardInterrupt:
    print("Monitoring CPU usage stopped.")
