import json
import logging
import os
from typing import Dict
import time

conf: Dict[str, any] = {
    "DEBUG_PROFILE": False,
    "SECRET_KEY": "HProxy-R-Salt",
    "REFRESH_INTERVAL": 86400,  # 24h刷新一次

    "WEBSITE_NAME": "ClashProxy",
    "WEBSITE_TITLE": "Clash-Proxy-神秘网站",

    "BASE_URL": [],
    "DOWNLOAD_URL": "123456789",
    "UA": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
          "Chrome/106.0.0.0 Mobile Safari/537.36",
    "DNS_URL": 0,
    "PROXY_URL": 1,

    "BASE_FILE_NAME": "base",
    "OUTPUT_FILE_NAME": "output",
    "DOWNLOAD_FILE_NAME": "ClashProxy",

    "MYSQL_URL": "localhost",
    "MYSQL_NAME": "localhost",
    "MYSQL_PASSWD": "123456",
    "MYSQL_PORT": 3306,
    "MYSQL_DATABASE": "clash",

    "LOG_HOME": "",
    "LOG_FORMAT": "[%(levelname)s]:%(name)s:%(asctime)s "
                  "(%(filename)s:%(lineno)d %(funcName)s) "
                  "%(process)d %(thread)d "
                  "%(message)s",
    "LOG_LEVEL": logging.INFO,
    "LOG_STDERR": True,

    "FOOT": "神秘网站",
    "LOGO": "logo.ico",
    "ICP": {}
}


def configure(conf_file: str, encoding="utf-8"):
    """ 运行配置程序, 该函数需要在其他模块被执行前调用 """
    with open(conf_file, mode="r", encoding=encoding) as f:
        json_str = f.read()
        conf.update(json.loads(json_str))

    if type(conf["LOG_LEVEL"]) is str:
        conf["LOG_LEVEL"] = {"debug": logging.DEBUG,
                             "info": logging.INFO,
                             "warning": logging.WARNING,
                             "error": logging.ERROR}.get(conf["LOG_LEVEL"])

    if len(conf["LOG_HOME"]) > 0:
        os.makedirs(conf["LOG_HOME"], exist_ok=True)

    conf["ID"] = str(time.time())
