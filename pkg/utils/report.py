import requests
import logging

version_str = "lqv0.0.1"

def report(count: int):
    try:
        res = requests.get("http://reports.rockchin.top:18989/usage?service_name=lightqchat&version={}&count={}&msg_source=cai".format(version_str, count))
        if res.status_code != 200 or res.text != "ok":
            logging.warning("report to server failed, status_code: {}, text: {}".format(res.status_code, res.text))
    except:
        return