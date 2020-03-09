# https://docs.gunicorn.org/en/stable/settings.html

bind = "0.0.0.0:5000"
workers = 8
max_requests = 2000
max_requests_jitter = 400
chdir = "/app"
worker_tmp_dir = "/dev/shm"
forwarded_allow_ips = "*"
proxy_allow_ips = "*"
