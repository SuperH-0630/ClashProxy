import yaml
import requests

from config import conf
from sql import db


ALLOW_PROXY_GROUP = ["手动选择", "全球直连", "规则之外"]
ALLOW_PROXY = ALLOW_PROXY_GROUP + ["DIRECT", "节点选择", "漏网之鱼"]
PROXY_2GROUP = ["全球直连", "漏网之鱼", "规则之外"]
METHODS = ['DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'IP-CIDR', 'IP-CIDR6', 'DOMAIN', 'GEOIP', 'MATCH']
DIRECT_OLD_RULE = ["DIRECT", "国内媒体", "哔哩哔哩", "网易云音乐", "微软云盘", "苹果服务", "谷歌FCM"]
DNS = {}
PROXY = {}
PROXY_GROUP = []


def change_proxy_group_name(name: str):
    if name == "漏网之鱼":
        return "规则之外"
    if name == "节点选择":
        return "手动选择"
    return name


def clean_base(base: dict, save_dns: bool, save_proxy: bool):
    global DNS, PROXY, PROXY_GROUP

    base["allow-lan"] = True  # 开启 allow-lan

    if save_dns:
        DNS = base["dns"]
    else:
        base["dns"] = DNS

    if save_proxy:
        for i in base["proxies"]:
            i["name"] = chinese_string(i["name"])
        PROXY = base["proxies"]

        new_proxies = []
        for i in base["proxy-groups"]:
            i["name"] = change_proxy_group_name(chinese_string(i["name"]))

            i["proxies"] = [chinese_string(a) for a in i["proxies"]]

            if i["name"] in ALLOW_PROXY_GROUP:
                if i["name"] in PROXY_2GROUP:  # 过滤 proxies
                    i["proxies"] = [change_proxy_group_name(n) for n in i["proxies"] if n in ALLOW_PROXY]
                new_proxies.append(i)

        base["proxy-groups"] = new_proxies
        PROXY_GROUP = new_proxies
    else:
        base["proxies"] = PROXY
        base["proxy-groups"] = PROXY_GROUP


def add_rule_to_sql(base: dict):
    for i in base["rules"]:
        m, *d = i.split(",")
        if m != "MATCH" and m != "GEOIP":
            d[1] = chinese_string(d[1])
            if d[1] in DIRECT_OLD_RULE:
                add_direct_rule_to_sql(m, *d)


def add_direct_rule_to_sql(method, address: str, _, no_resolve=False):
    address = address.strip()
    no_resolve = no_resolve == "no-resolve"
    method_num = METHODS.index(method)
    res = db.search(r"SELECT id FROM chinese WHERE methods = %s AND address = %s", method_num, address)
    if res is not None and res.rowcount > 0:
        return False

    db.insert("INSERT INTO chinese(methods, address, no_resolve) VALUES(%s, %s, %s)",
              method_num, address, no_resolve)
    return True



def get_rule_from_sql(base: dict):
    rules = []
    res = db.search(r"SELECT methods, address, no_resolve FROM chinese")
    if res is None:
        return

    for i in res:
        if i[2]:
            rule = f"{METHODS[i[0]]},{i[1]},全球直连,no-resolve"
        else:
            rule = f"{METHODS[i[0]]},{i[1]},全球直连"
        rules.append(rule)
    rules.append("GEOIP,CN,全球直连")
    rules.append("MATCH,规则之外")
    base["rules"] = rules


def chinese_string(text: str):
    for i in text:
        if ord(i) >= 127 and not 0x4E00 <= ord(i) <= 0x9FA5:
            text = text.replace(i, "")
        if ord(i) <= 31:
            text = text.replace(i, "")
    return text.strip()


def get_rule_file(save_dns: bool,
                  save_proxy: bool,
                  save_rule: bool,
                  base_file: str = "base.yaml",
                  output_file: str | None = "output.yaml"):
    with open(base_file, mode="r", encoding="utf-8") as f:
        base: dict = yaml.load(f, yaml.Loader)

    if save_dns or save_rule or output_file is not None:
        clean_base(base, save_dns, save_proxy)

    if save_rule:
        add_rule_to_sql(base)

    if output_file is not None:
        get_rule_from_sql(base)

        with open(output_file, mode="w", encoding="utf-8") as f:
            yaml.dump(base, f)


def download_base_file(base_url: str, base_file: str = "base.yaml"):
    response = requests.get(url=base_url, headers={"User-Agent": conf["UA"]})
    with open(base_file, mode="wb") as f:
        f.write(response.content)


def make_output_file(download: bool = True):
    url = conf["BASE_URL"]
    save_dns = conf["DNS_URL"]
    save_proxy = conf["PROXY_URL"]
    save_rule = conf["RULE_URL"]

    for i in range(len(url)):
        if download:
            try:
                download_base_file(url[i], base_file=f"{conf['BASE_FILE_NAME']}{i}.yaml")
            except requests.exceptions.RequestException:
                pass

        try:
            get_rule_file(save_dns=(save_dns == i),
                          save_proxy=(save_proxy == i),
                          save_rule=(i in save_rule),
                          base_file=f"{conf['BASE_FILE_NAME']}{i}.yaml",
                          output_file=(f"{conf['OUTPUT_FILE_NAME']}.yaml" if i == len(url) - 1 else None))
        except FileNotFoundError:
            pass
