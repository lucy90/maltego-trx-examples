import logging

from splunklib.client import Service, connect

HOST = "localhost"
PORT = 8089


class SplunkServiceException(Exception):
    pass


class SplunkServiceError(Exception):
    pass


class SplunkService:
    log = logging.getLogger(__name__)

    @staticmethod
    def session_key_login(session_key: str) -> Service:
        # Create a Service instance and log in
        service: Service = connect(
            host=HOST,
            port=PORT,
            token=session_key)

        return service.connect()
