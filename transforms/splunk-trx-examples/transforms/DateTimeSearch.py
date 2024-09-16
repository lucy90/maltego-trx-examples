from __future__ import annotations
import datetime

from typing import Dict
from extensions import registry
from maltego_trx.maltego import UIM_TYPES, MaltegoMsg, MaltegoTransform, UIM_INFORM
from maltego_trx.decorator_registry import TransformSetting
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.entities import Phrase
from entities.SplunkEventEntity import SplunkEventEntity

from splunk_api_full.splunk_client import SplunkService
from splunklib.results import Message
from settings import token_global_setting


splunk_example_daterange_setting = TransformSetting(
        name="splunk_example_daterange",
        display_name="Date Range",
        setting_type="daterange",
        popup=True
)

splunk_date_format_string = "%Y-%m-%dT%H:%M:%S"


class DateRange(object):

    def __init__(self, start=None, end=None):
        if start is not None or end is not None:
            if None in (start, end):
                raise ValueError("Must specify both 'start' and 'end' (or 'range')")
        self.start = start
        self.end = end

    @classmethod
    def fromstring(cls, date_range_string: str) -> DateRange:
        if date_range_string.startswith(".") or date_range_string[0].isdigit():  # 1615480642.730-1623256642.730
            start, end = date_range_string.split("-")
            if start == ".000":  # bug in Maltego Client e.g. .000 - 1623256642.730
                start = 1  # splunk expects 1 if time is since unix epoch
                end = "now"  # if start is 1,  we set end to now, as that is what is implied in Maltego Client
            else:
                start, end = float(start), float(end)
                start, end = datetime.datetime.fromtimestamp(start), datetime.datetime.fromtimestamp(end)
                start, end = start.strftime(splunk_date_format_string), end.strftime(splunk_date_format_string)
            return DateRange(start, end)
        raise ValueError("Cannot parse DateRange input, sorry.")


@registry.register_transform(display_name="DateTime Range Search",
                             input_entity=Phrase,
                             description="Perform a datetime range search query on Splunk.",
                             output_entities=[Phrase],
                             settings=[token_global_setting, splunk_example_daterange_setting])
class DateTimeSearch(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        try:
            token = request.getTransformSetting(token_global_setting.name)
            count = request.Slider
            date_range = request.getTransformSetting(splunk_example_daterange_setting.name)


            try:
                date_range: DateRange = DateRange.fromstring(date_range)
            except ValueError:
                message = f"Invalid DateRange"
                response.addUIMessage(message, UIM_INFORM)
                return

            earliest_time = date_range.start
            latest_time = date_range.end

            input_value = request.Value

            if not input_value:
                response.addUIMessage(f"Invalid input {request.Type}")
                return

            # query to retrieve results from main
            splunk_query = f"search index=main"

            results = SplunkService.run_splunk_search(
                token=token,
                query=splunk_query,
                count=count,
                earliest_time=earliest_time,
                latest_time=latest_time
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
