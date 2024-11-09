# Smart Parking Server

This is the server side of the Smart Parking project.

## Installation

1. Clone the repository
2. Run `pip install -r requirements.txt` or `pip3 install -r requirements.txt` to install the required packages
3. Run `python manage.py runserver 0.0.0.0:8000` or `python3 manage.py runserver 0.0.0.0:8000` to start the server

## Discovered Issues

Firewall need to allow inbound and outbound traffic on port 8000. 

For linux users, this can be done by running the following command:

```bash
sudo ufw enable # to enable the firewall during startup
sudo ufw allow 8000 # to allow traffic on port 8000
```

For windows users, you can follow the steps in this [article](https://www.tomshardware.com/news/how-to-open-firewall-ports-in-windows-10,36451.html).
