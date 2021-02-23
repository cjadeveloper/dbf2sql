import configparser

from pathlib import Path

import click


def create_config_file(path):
    """Create config.ini file"""
    click.secho(
        "\nCreates a basic config.ini file in the current directory if doesn't exist",
        fg="bright_blue",
    )

    config = configparser.ConfigParser()

    config.add_section("dbf")
    config.set("dbf", "path", "")
    config.set("dbf", "encoding", "cp1252")

    config.add_section("dbcnx")
    config.set("dbcnx", "cnxstring", "")

    try:
        with open(path, "w") as ini_file:
            config.write(ini_file)
            print("<°o°> Hooray! config.ini file has been created!")
    except IOError:
        print("<`-´> Ouch! An IOError has occurred while config.ini file was created!")


def _get_config(path):
    """Return the config object"""

    if not Path(path).exists():
        create_config_file(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_config_setting(path, section, setting, fallback=None):
    """Print out a setting and return a value"""

    config = _get_config(path)
    value = config.get(section, setting, fallback=fallback)
    return value


def list_config_setting(path):
    try:
        config_file = open(path, "r")
        click.secho("\nList the current configuration:", fg="bright_blue")
        print()
        for line in config_file:
            print(line, end="")
    except IOError:
        print("\n<`-´> Ouch! An IOError has occurred!")
    finally:
        config_file.close()


def update_config_setting(path, section, setting, value):
    """Update a config setting"""

    config = _get_config(path)
    config.set(section, setting, value)
    try:
        with open(path, "w") as ini_file:
            config.write(ini_file)
    except IOError:
        print("\n<`-´> Ouch! An IOError has occurred!")
    finally:
        config.close()


def delete_config_setting(path, section, setting):
    """Delete a config setting"""

    config = _get_config(path)
    config.remove_option(section, setting)
    try:
        with open(path, "w") as ini_file:
            config.write(ini_file)
    except IOError:
        print("\n<`-´> Ouch! An IOError has occurred!")
    finally:
        config.close()
