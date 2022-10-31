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
from clash import download_base_file, get_rule_file


def start():
    url = conf["BASE_URL"]
    save_dns = conf["DNS_URL"]
    save_proxy = conf["PROXY_URL"]

    for i in range(len(url)):
        try:
            download_base_file(url[i], base_file=f"{conf['BASE_FILE_NAME']}.yaml")
        except requests.exceptions.RequestException:
            pass

        try:
            get_rule_file(save_dns=(save_dns == i),
                          save_proxy=(save_proxy == i),
                          base_file=f"{conf['BASE_FILE_NAME']}.yaml",
                          output_file=f"{conf['OUTPUT_FILE_NAME']}.yaml")
        except FileNotFoundError:
            pass


app = ClashFlask(__name__)


class FirstRefresh(threading.Thread):
    def __init__(self):
        super(FirstRefresh, self).__init__()
        self.daemon = True  # 设置为守护进程

    def run(self):
        start()


class TimerRefresh(threading.Timer):
    def __init__(self):
        super(TimerRefresh, self).__init__(conf["REFRESH_INTERVAL"], start)
        self.daemon = True  # 设置为守护进程


if __name__ == '__main__':
    start()
else:
    # 作为Flask启动
    FirstRefresh().start()
    TimerRefresh().start()
