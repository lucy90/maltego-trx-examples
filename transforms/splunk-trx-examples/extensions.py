from maltego_trx.decorator_registry import TransformRegistry

registry = TransformRegistry(
        owner="Maltego",
        author="Lucia Rodrigues <lvr@maltego.com>",
        host_url="http://192.168.1.209:8080",
        seed_ids=["splunktrxexamples"]
)

# The rest of these attributes are optional

# metadata
registry.version = "0.1"

# global settings
# from maltego_trx.template_dir.settings import api_key_setting
# registry.global_settings = [api_key_setting]

# transform suffix to indicate datasource
registry.display_name_suffix = " [Splunk Examples]"

# reference OAuth settings
# registry.oauth_settings_id = ['github-oauth']
