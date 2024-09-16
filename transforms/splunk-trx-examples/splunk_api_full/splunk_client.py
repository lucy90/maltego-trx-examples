import logging

from splunklib import results
from splunklib.binding import AuthenticationError, HTTPError
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
    def bearer_token_login(token: str) -> Service:
        # Create a Service instance and log in
        service: Service = connect(
            host=HOST,
            port=PORT,
            splunkToken=token)
        return service

    @classmethod
    def run_splunk_search(cls, token, query, earliest_time=None, latest_time=None, count=100):

        try:
            service: Service = cls.bearer_token_login(token)

            search_results = service.jobs.oneshot(query, count=count, earliest_time=earliest_time,
                                                  latest_time=latest_time)
            # Get the results and process them using the ResultsReader
            results_stream = results.ResultsReader(search_results)
            cls.log.debug("Successfully retrieved search results from Splunk service")
            return results_stream

        except AuthenticationError as auth_error:
            message = f"Incorrect login credentials whilst logging into Splunk Instance: {str(auth_error)}"
            cls.log.error(message, extra={"operation": "splunk_auth"})
            raise SplunkServiceError(message) from auth_error
        except HTTPError as http_error:
            message = f"HTTP Connection error whilst connecting to Splunk Instance from Transform Server: {str(http_error)}"
            cls.log.error(message, extra={"operation": "splunk_http"})
            raise SplunkServiceError(message) from http_error
        except (ValueError, TypeError) as api_error:
            message = f"Splunk Instance returned as error: {str(api_error)}"
            cls.log.error(message, extra={"operation": "splunk_api"})
            raise SplunkServiceError(message) from api_error
        except Exception as e:
            message = f"Error connecting to Splunk API: {str(e)}"
            cls.log.exception(message, extra={"operation": "splunk_api"})
            raise SplunkServiceException(message) from e
