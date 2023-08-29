from django.core.exceptions import ImproperlyConfigured
from requests.exceptions import ConnectionError, HTTPError


class DataverseConfigurationError(ImproperlyConfigured):
    """
    Raised when the DATAVERSE_* Django project settings are missing
    or incomplete.
    """

    pass


class DataverseMissingSettingError(DataverseConfigurationError):
    """
    Raised when a specific setting is missing from the Django project
    settings or environment variables.
    """

    pass


class DataverseInvalidSettingValueError(DataverseConfigurationError):
    """
    Raised when a specific setting is present for the Django project
    or environment, but doos not have a valid value.
    """

    pass


class DataverseAuthenticationError(HTTPError):
    """
    Raised when the Dataverse API client cannot contact the
    authentication vendor endpoint or the combination of details
    sent to it are invalid.
    """

    pass


class DataverseConnectionError(ConnectionError):
    """
    Raised when the Dataverse API client cannot reach the the
    Dataverse Web API (usually due to a network connection issue,
    or incorrect DATAVERSE_API_HOSTNAME setting value).
    """

    pass


class DataverseHttpError(HTTPError):
    """
    Raised when the Dataverse Web API responds with a 403 or 401 status
    code (indicating a user )
    """

    pass


class DataverseRowDoesNotExist(DataverseHttpError):
    """
    Raised when a request for data from the Dataverse Web API results
    in a 404 error response. Or, when requesting multiple rows at once,
    and no item matching a specific ID value was found.
    """

    pass


class DataverseUserPermissionError(DataverseHttpError):
    """
    Raised when a Dataverse Web API response has a status code of
    403 or 401 (indicating a user configuration issue on the
    Dataverse / Azure side).
    """

    pass
