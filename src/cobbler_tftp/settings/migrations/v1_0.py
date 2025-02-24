"""Module for the validation, normalization and migration of the schema version "1.0"."""

from pathlib import Path

from schema import Optional, Or, Schema, SchemaError, SchemaWrongKeyError

from cobbler_tftp.types import SettingsDict

settings_schema: Schema = Schema(
    {
        Optional("schema"): float,
        Optional("auto_migrate_settings"): bool,
        Optional("is_daemon"): bool,
        Optional("cobbler"): {
            Optional("uri"): str,
            Optional("username"): str,
            Optional(Or("password", "password_file", only_one=True)): Or(str, Path),
        },
    }
)


def validate(settings_dict: SettingsDict) -> bool:
    """
    Validate the given dictionary of configuration parameters to the reference ``schema``.

    :param settings_dict: The dictionary of configuration parameters to validate
    :return bool: True/False depending on whether the dicts match or not
    """
    if settings_dict == {} or settings_dict is None:
        return False

    try:
        settings_schema.validate(settings_dict)
    except (SchemaError, SchemaWrongKeyError) as exc:
        print(exc)
        return False
    return True


def normalize(settings_dict: SettingsDict) -> SettingsDict:
    """
    If data in ``settings_dict`` is valid, the validated data is returned.

    :param settings_dict: The dictionary of configuration parameters to validate
    :return: the validated dict
    :rtype dict:
    """
    return settings_schema.validate(settings_dict)


def migrate(settings_dict: SettingsDict) -> SettingsDict:
    """
    Migrate settings dict from previous to current version.

    :param settings_dict: The dictionary to migrate
    :return: The settings dict
    """
    if not validate(settings_dict):
        raise SchemaError("v1.0.0: Schema error while validating")
    return normalize(settings_dict)
