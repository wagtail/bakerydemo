import os

from django.conf import settings

from .client import DataverseClient
from .exceptions import DataverseInvalidSettingValueError, DataverseMissingSettingError


def get_required_setting(setting_name):
    try:
        value = getattr(settings, setting_name)
    except AttributeError:
        try:
            value = os.environ.get(setting_name)
        except KeyError:
            raise DataverseMissingSettingError(
                "No {} value can be found for this project/environment. Please add it to your project setings or environment variables.".format(
                    setting_name
                )
            )

    if not value or (isinstance(value, str) and not value.strip()):
        raise DataverseInvalidSettingValueError(
            "'{0}' is not a valid value for {1}. Ask a colleuge for the right value to use here.".format(
                value, setting_name
            )
        )

    return value


def get_api_client():
    kwargs = dict(
        api_hostname=get_required_setting("DATAVERSE_API_HOSTNAME"),
        api_version=get_required_setting("DATAVERSE_API_VERSION"),
        client_id=get_required_setting("DATAVERSE_API_CLIENT_ID"),
        tenant_id=get_required_setting("DATAVERSE_API_TENANT_ID"),
        client_secret=get_required_setting("DATAVERSE_API_CLIENT_SECRET"),
    )
    return DataverseClient(**kwargs)
