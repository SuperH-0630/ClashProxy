import os
import logging
import threading
import requests.exceptions

from config import configure, conf


env_dict = os.environ
conf_file = env_dict.get("CLASH_PROXY_CONF")
if conf_file is None:
    logging.info("Configure file ./etc/conf.json")
    configure("./etc/conf.json")
else:
    logging.info(f"Configure file {conf_file}")
    configure(conf_file)


from app import ClashFlask
from clash import make_output_file


app = ClashFlask(__name__)


class FirstRefresh(threading.Thread):
    def __init__(self):
        super(FirstRefresh, self).__init__()
        self.daemon = True  # 设置为守护进程

    def run(self):
        make_output_file()


class TimerRefresh(threading.Timer):
    def __init__(self):
        super(TimerRefresh, self).__init__(conf["REFRESH_INTERVAL"], make_output_file)
        self.daemon = True  # 设置为守护进程


if __name__ == '__main__':
    make_output_file()
else:
    # 作为Flask启动
    FirstRefresh().start()
    TimerRefresh().start()
