from typing import Dict
from datetime import datetime, timedelta
from extensions import registry
from maltego_trx.maltego import UIM_TYPES, MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.entities import Phrase
from entities.SplunkEventEntity import SplunkEventEntity
from splunk_api_full.splunk_client import SplunkService
from splunklib.results import Message
from settings import token_global_setting


@registry.register_transform(display_name="Base Search",
                             input_entity=Phrase,
                             description="Perform a search query on the main index on Splunk for the last 2 years.",
                             output_entities=[Phrase],
                             settings=[token_global_setting])
class BaseSearch(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        try:
            splunk_date_format_string = "%Y-%m-%dT%H:%M:%S"

            # getting the start date being 2 years from now, you can set it to whatever you want it to be
            start_date = datetime.now() - timedelta(days=365*2)
            splunk_start_date = start_date.strftime(splunk_date_format_string)

            # getting the current date and time
            current_datetime = datetime.now()

            # getting the year from the current date and time
            splunk_end_date = current_datetime.strftime(splunk_date_format_string)

            token = request.getTransformSetting(token_global_setting.name)
            input_value = request.Value
            count = request.Slider

            if not input_value:
                response.addUIMessage(f"Invalid input {request.Type}")
                return

            # query to retrieve results from main in the last two years
            splunk_query = f"search index=main"

            results = SplunkService.run_splunk_search(
                token=token,
                query=splunk_query,
                count=count,
                earliest_time=splunk_start_date,
                latest_time=splunk_end_date
            )

            for result in results:
                if isinstance(result, Dict):
                    raw_value = result.get("raw", "").replace("\n", " ")
                    entity = SplunkEventEntity()
                    entity.setValue(raw_value)
                    entity.set_generic_properties(result)
                    entity.set_meta()
                    response.entities.append(entity)
                elif isinstance(result, Message):
                    response.addUIMessage(f"Splunk Message: {result}")

        except Exception as e:
            response.addUIMessage(f"Error: {e}", UIM_TYPES["partial"])
