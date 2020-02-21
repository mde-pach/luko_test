import requests

class SimpleLaposteClient():
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {}

    def get(self, resource):
        res = requests.get(
            "{base_url}/{resource}".format(base_url=self.base_url, resource=resource),
            headers=self.headers
        )
        res.raise_for_status()
        return res
