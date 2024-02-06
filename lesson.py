import requests
import json
from websockets.sync.client import connect
from websockets.exceptions import ConnectionClosed, ConnectionClosedOK
from time import sleep
from tools import seconds_until_target_time
from config import LOGGER, SESSION_DATA


class Lesson:
    def __init__(self, starttime: str, endtime: str, token: str):
        self.headers = {
            "authority": "api.mycdn.me",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

        self.starttime = starttime
        self.endtime = endtime
        self.token = token

    def get_session(self) -> None:
        data = {
            "session_data": SESSION_DATA,
            "method": "auth.anonymLogin",
            "format": "JSON",
            "application_key": "CFJCCIJGDIHBABABA",
        }

        response = requests.post(
            "https://api.mycdn.me/fb.do", headers=self.headers, data=data
        )

        res_data: dict = json.loads(response.text)

        self.session: str = res_data.get("session_key")

    def get_link(self) -> None:
        data = {
            "joinLink": self.token,
            "isVideo": "false",
            "protocolVersion": "5",
            "method": "vchat.joinConversationByLink",
            "format": "JSON",
            "application_key": "CFJCCIJGDIHBABABA",
            "session_key": self.session,
        }

        response = requests.post(
            "https://api.mycdn.me/fb.do", headers=self.headers, data=data
        )
        res_data = json.loads(response.text)

        link: str = (
            res_data["endpoint"]
            + "&platform=WEB&appVersion=1.1&version=5&device=browser&capabilities=97F&clientType=VK&tgt=join"
        )
        self.link = link

    def start(self) -> None:
        delta_seconds = seconds_until_target_time(self.starttime)
        LOGGER.debug(delta_seconds)
        LOGGER.info(f"Connecting to the lesson in {delta_seconds} seconds")

        sleep(delta_seconds)

        self.get_session()
        LOGGER.info(f"Session started")
        self.get_link()
        LOGGER.info(f"The WS link has been received")
        LOGGER.info("Connected to the lesson")

        websocket = connect(self.link)

        LOGGER.debug(websocket.recv())
        websocket.send(
            """{
                "command": "change-media-settings",
                "sequence": 1,
                "mediaSettings": {
                    "isAudioEnabled": false,
                    "isVideoEnabled": false,
                    "isScreenSharingEnabled": false,
                    "isFastScreenSharingEnabled": false,
                    "isAudioSharingEnabled": false,
                    "isAnimojiEnabled": false
                }
            }"""
        )
        LOGGER.info("The settings are set")
        LOGGER.debug(websocket.recv())

        LOGGER.info("Listening to the server")
        while (
            seconds_until_target_time(self.endtime) > 1.0
            and seconds_until_target_time(self.endtime) < 2740.0
        ):
            try:
                LOGGER.debug(websocket.recv(), seconds_until_target_time(self.endtime))
                websocket.pong(b"pong")
            except (ConnectionClosed, ConnectionClosedOK):
                LOGGER.info("Connection closed, reconnecting")
                websocket = connect(self.link)
                LOGGER.info("Reconnected")
                continue

        websocket.send(
            """{
                "command": "hangup",
                "sequence": 5,
                "reason": "HUNGUP"
            }"""
        )

        LOGGER.info("Leaving the lesson")
        LOGGER.debug(websocket.recv())
        websocket.close()
