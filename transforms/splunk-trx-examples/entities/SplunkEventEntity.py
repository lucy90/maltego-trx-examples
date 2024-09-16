from typing import Dict, Any

from maltego_trx.maltego import MaltegoEntity


class SplunkEventEntity(MaltegoEntity):
    raw: str
    unique_id: str
    bucket_id: str
    time: str

    @classmethod
    def get_annotations(cls):  # hack to get entity parent class fields for xml generation
        all_annotations: Dict[str, Any] = {}
        for clazz in cls.mro():
            try:
                all_annotations.update(**clazz.__annotations__)
            except AttributeError:
                pass
        return all_annotations

    def set_meta(self):
        self.setType(self.Meta.id)

    def set_properties(self, iterable, cim_model_name):
        for field_name, field_value in iterable.items():
            if field_name == "_time":
                field_name = "time"
            clean_name = field_name.replace(cim_model_name + ".", "")
            self.__setattr__(clean_name, field_value)
            if field_value != "none" and field_value != "unknown":
                self.addProperty(fieldName=clean_name,
                                 # displayName=beautify_name(clean_name),
                                 displayName=clean_name,
                                 matchingRule="strict",
                                 value=field_value, )

    def set_generic_properties(self, iterable):
        for field_name, field_value in iterable.items():
            if field_name == "_time":
                field_name = "time"
            self.__setattr__(field_name, field_value)
            if field_value != "none" and field_value != "unknown":
                self.addProperty(fieldName=field_name,
                                 #displayName=beautify_name(field_name),
                                 displayName=field_name,
                                 matchingRule="strict",
                                 value=field_value, )

    class Meta:
        id = "maltego.splunk.BaseEvent"
        display_name = "Splunk Base Event"
        display_name_plural = "Splunk Base Event"
        description = "Splunk Base Event"
        category = "Splunk Entities"
        small_icon_resource = "Custom/Splunk"
        large_icon_resource = "Custom/Splunk"
        allowed_root = "False"
        conversion_order = "2147483647"
        visible = "true"
        has_parent = False
        parent = ""