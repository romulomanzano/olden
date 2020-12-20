import requests
import config


class CallOrchestrator:
    def __init__(self):
        self.base_url = config.DAILY_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(config.DAILY_API_KEY),
        }

    def create_room(self):
        url = "{}/v1/rooms".format(self.base_url)
        response = requests.request("POST", url, headers=self.headers)
        print(response.text)
