from typing import Dict
from extensions import registry
from maltego_trx.maltego import UIM_TYPES, MaltegoMsg, MaltegoTransform, UIM_PARTIAL
from maltego_trx.decorator_registry import TransformSetting
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.entities import Phrase
from entities.SplunkEventEntity import SplunkEventEntity

from splunk_api_full.splunk_client import SplunkService
from splunklib.results import Message
from settings import token_global_setting


splunk_example_search_input_setting = TransformSetting(
        name="splunk_example_search_input",
        display_name="Splunk field which search results using the given value",
        setting_type="string",
        popup=True
)


@registry.register_transform(display_name="Search for a particular value",
                             input_entity=Phrase,
                             description="Retrieve results from a given value.",
                             output_entities=[Phrase],
                             settings=[token_global_setting, splunk_example_search_input_setting])
class WhereSearch(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        try:
            token = request.getTransformSetting(token_global_setting.name)
            count = request.Slider
            splunk_sort_field_name = request.getTransformSetting(splunk_example_search_input_setting.name)

            if not splunk_sort_field_name:
                message = "Missing 'splunk search value' in transform settings"
                response.addUIMessage(message, UIM_PARTIAL)
                return

            # query to retrieve results from main index sorted by given field name
            splunk_query = f"search index=main | earliest=-2y and latest=now | sort {splunk_sort_field_name}"

            results = SplunkService.run_splunk_search(
                token=token,
                query=splunk_query,
                count=count
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
