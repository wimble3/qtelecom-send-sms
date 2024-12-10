import logging

import requests

from abc import ABC, abstractmethod


from app.libs.requests.qtsms.exceptions import (
    QTLengthTooLongException, QTEmptySMSException, QTError)


class IQuickTelecomService(ABC):
    """Interface for quick telecom outer service."""
    @abstractmethod
    def post_sms(
            self,
            targets: list[str],
            message: str,
            sender: str = ""
    ) -> None:
        """
        Process of sending request to quick telecom outer service for sms.
        """


class QuickTelecomService:
    """Service for working with requests to quick telecom outer service."""
    HEADERS = {
        "User-Agent": "qtelecom.ru python API client",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    SEND_SMS_URL = "https://go.qtelecom.ru/public/http/"
    START_BODY = {
        "action": "post_sms",
        "sms_type": ""
    }

    def __init__(self, user: str, password: str) -> None:
        """Initializes params."""
        self.__user = user
        self.__password = password

    def post_sms(
            self,
            targets: list[str],
            message: str,
            sender: str = ""
    ) -> None:
        """
        Process of sending request to quick telecom outer service for sms.
        """
        if len(message) > 480:
            raise QTLengthTooLongException(
                "SMS length is too long, max: 480 symbols")

        if len(message) <= 0:
            raise QTEmptySMSException("SMS is empty")

        body = {
            "target": ",".join(targets),
            "sender": sender,
            "user": self.__user,
            "pass": self.__password,
            "message": message
        }
        body.update(self.START_BODY)

        with requests.post(
                self.SEND_SMS_URL,
                data=body,
                headers=self.HEADERS
        ) as response:
            response_text = response.text
            if response.status_code != 200:
                raise QTError(
                    f"Request failed with status code "
                    f"{response.status_code}\n"
                    f"XML response: {response_text}"
                )
            logging.info(
                f"Message '{message}' has been sent by targets {targets}\n"
                f"XML response: {response_text}"
            )
