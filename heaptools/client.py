import json
import requests


class HeapAPIClient():
    def __init__(self, app_id):
        """

        :param app_id: Heap analytics app_id
        :type app_id: str
        """

        self.base_url = "https://heapanalytics.com/api"
        self.app_id = app_id

        if app_id is None:
            raise RuntimeError("app_id must be valid!")

    def track(self, identity=None, event=None, properties=None):
        """
        Post a "track" event to the Heap Analytics API server
        :param identity: user identity
        :type identity: str
        :param event: event name
        :type event: str
        :param properties: optional, additional event properties
        :type properties: dict
        """

        if identity is None or event is None:
            raise RuntimeError("identity and event must be valid!")

        data = {
            "app_id": self.app_id,
            "identity": identity,
            "event": event
        }

        if properties is not None:
            data["properties"] = properties

        return requests.post(self.base_url + '/track', data=json.dumps(data), headers={'Content-Type': 'application/json'})

    def add_user_properties(self, identity=None, properties=None):
        """
        Post a "add_user_properties" event to the Heap Analytics API server
        :param identity: user identity
        :type identity: str
        :param properties: optional, additional properties to associate with the user
        :type properties: dict
        """

        if identity is None:
            raise RuntimeError("identity must be valid!")

        data = {
            "app_id": self.app_id,
            "identity": identity,
        }

        if properties is not None:
            data["properties"] = properties

        return requests.post(self.base_url + '/add_user_properties', data=json.dumps(data),
                             headers={'Content-Type': 'application/json'})

    def bulk_add_user_properties(self, bulk):
        """
        Post a "add_user_properties" event to the Heap Analytics API server
        :param identity: user identity
        :type identity: str
        :param properties: optional, additional properties to associate with the user
        :type properties: dict
        """

        data = {
            "app_id": self.app_id,
            "users": bulk,
        }

        return requests.post(self.base_url + '/add_user_properties', data=json.dumps(data),
                             headers={'Content-Type': 'application/json'})
