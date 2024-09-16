from extensions import registry
from maltego_trx.maltego import UIM_TYPES, MaltegoMsg, MaltegoTransform
from maltego_trx.decorator_registry import TransformSetting
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.entities import Phrase
from splunk_api_auth.username_password import SplunkService


username_setting = TransformSetting(
    name="splunk_example_username",
    display_name="Splunk Username",
    setting_type="string",
    optional=False,
    popup=True)


password_setting = TransformSetting(
    name="splunk_example_password",
    display_name="Splunk Password",
    setting_type="string",
    optional=False,
    popup=True)


@registry.register_transform(
    display_name="Username Password Authentication",
    input_entity=Phrase,
    description="Connect to the Splunk API using username and password authentication.",
    output_entities=[Phrase],
    settings=[username_setting, password_setting],
    transform_set="Auth"
)
class UsernamePasswordAuth(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        try:
            username = request.getTransformSetting(username_setting.name)
            password = request.getTransformSetting(password_setting.name)

            if not username:
                response.addUIMessage(f"Username is required")
                return

            if not password:
                response.addUIMessage(f"Password is required")
                return

            results = SplunkService.username_password_login(
                username=username,
                password=password
            )

            if results:
                response.addEntity(Phrase, "success")

        except Exception as e:
            response.addUIMessage(f"Error: {e}", UIM_TYPES["partial"])
            response.addEntity(Phrase, "fail")
