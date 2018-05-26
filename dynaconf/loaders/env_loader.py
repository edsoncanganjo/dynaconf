# coding: utf-8
import os
from dynaconf.utils.parse_conf import parse_conf_data
from dotenv import cli as dotenv_cli

IDENTIFIER = 'env'


def load(obj, env=None, silent=True, key=None):
    """Loads envvars with prefixes:
    DYNACONF_ (default global) or $(GLOBAL_ENV_FOR_DYNACONF)_
    """
    global_env = obj.get('GLOBAL_ENV_FOR_DYNACONF')
    if global_env.upper() != 'DYNACONF':
        load_from_env(
            IDENTIFIER + '_global',
            key,
            'DYNACONF',
            obj,
            silent
        )

    # Load the global env if exists and overwrite everything
    load_from_env(
        IDENTIFIER + '_global',
        key,
        global_env,
        obj,
        silent
    )


def load_from_env(identifier, key, env, obj, silent):
    env = env.upper()  # noqa
    env_ = '{0}_'.format(env)  # noqa
    try:
        if key:
            value = os.environ.get(
                '{0}_{1}'.format(env, key)
            )
            if value:
                obj.logger.debug(
                    "env_loader:loading by key: %s:%s (%s)",
                    key,
                    value,
                    identifier
                )
                obj.set(key, value, loader_identifier=identifier)
        else:
            data = {
                key.partition(env_)[-1]: parse_conf_data(data)
                for key, data
                in os.environ.items()
                if key.startswith(env_)
            }
            obj.logger.debug(
                "env_loader:loading:%s (%s)",
                data,
                identifier
            )
            obj.update(data, loader_identifier=identifier)
    except Exception as e:  # pragma: no cover
        e.message = (
            'Unable to load config env env ({0})'
        ).format(str(e))
        if silent:
            obj.logger.error(str(e))
        else:
            raise


def write(settings_path, settings_data, **kwargs):
    for key, value in settings_data.items():
        dotenv_cli.set_key(
            str(settings_path),
            key.upper(),
            value
        )
