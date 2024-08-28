import socket
from datetime import datetime
from gw.common import database
from gw.reporter import metrics


def main():
    database.connect()
    database.select("metric_db")
    time_var = datetime.now()
    data = {
        'timestamp': time_var.strftime("%Y-%m-%d %H:%M"),
        'hostname': socket.gethostname(),
        'metrics': metrics.get_metrics()
    }
    database.add_record(data)


if __name__ == "__main__":
    main()

