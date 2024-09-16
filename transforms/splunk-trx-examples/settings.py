from maltego_trx.decorator_registry import TransformSetting

api_key_setting = TransformSetting(name='api_key',
                                   display_name='API Key',
                                   setting_type='string',
                                   global_setting=True)


token_global_setting = TransformSetting(
    name="global#splunk_example_token",
    display_name="Splunk Token",
    setting_type="string",
    optional=True,
    popup=True)