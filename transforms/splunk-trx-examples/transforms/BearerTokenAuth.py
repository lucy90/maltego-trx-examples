from extensions import registry
from maltego_trx.maltego import UIM_TYPES, MaltegoMsg, MaltegoTransform
from maltego_trx.decorator_registry import TransformSetting
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.entities import Phrase
from splunk_api_auth.bearer_token import SplunkService


bearer_token_setting = TransformSetting(
    name="splunk_example_bearer_token",
    display_name="Splunk Token",
    setting_type="string",
    optional=False,
    popup=True)


@registry.register_transform(
    display_name="Bearer Token Authentication",
    input_entity=Phrase,
    description="Connect to the Splunk API using bearer token authentication.",
    output_entities=[Phrase],
    settings=[bearer_token_setting],
    transform_set="Auth"
)
class BearerTokenAuth(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        try:
            token = request.getTransformSetting(bearer_token_setting.name)

            if not token:
                response.addUIMessage(f"Bearer token is required")
                return

            results = SplunkService.bearer_token_login(
                token=token
            )

            if results:
                response.addEntity(Phrase, "success")

        except Exception as e:
            response.addUIMessage(f"Error: {e}", UIM_TYPES["partial"])
            response.addEntity(Phrase, "fail")
