# Run headless

locust -f main.py --headless -u 1000 -r 50 --run-time 5m --host http://192.168.0.6:8000 --csv django --csv-full-history
