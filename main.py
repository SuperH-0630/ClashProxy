import os
import logging

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
    download_base_file(f"{conf['BASE_FILE_NAME']}.yaml")
    get_rule_file(f"{conf['BASE_FILE_NAME']}.yaml", f"{conf['OUTPUT_FILE_NAME']}.yaml")


app = ClashFlask(__name__)


if __name__ == '__main__':
    start()
