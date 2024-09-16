from extensions import registry
from maltego_trx.maltego import UIM_TYPES, MaltegoMsg, MaltegoTransform
from maltego_trx.decorator_registry import TransformSetting
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.entities import Phrase
from splunk_api_auth.session_key import SplunkService


session_key_setting = TransformSetting(
    name="splunk_example_session_key",
    display_name="Splunk Token",
    setting_type="string",
    optional=False,
    popup=True)


@registry.register_transform(
    display_name="Session Key Authentication",
    input_entity=Phrase,
    description="Connect to the Splunk API using session key authentication.",
    output_entities=[Phrase],
    settings=[session_key_setting],
    transform_set="Auth"
)
class SessionKeyAuth(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        try:
            session_key = request.getTransformSetting(session_key_setting.name)

            if not session_key:
                response.addUIMessage(f"Session key is required")
                return

            results = SplunkService.session_key_login(
                session_key=session_key
            )

            if results:
                response.addEntity(Phrase, "success")

        except Exception as e:
            response.addUIMessage(f"Error: {e}", UIM_TYPES["partial"])
            response.addEntity(Phrase, "fail")
