from pathlib import Path
from pathlib import PurePosixPath

import click

from .__version__ import __version__
from .config.settings import create_config_file
from .config.settings import get_config_setting
from .config.settings import list_config_setting

# Directorio Raíz del proyecto
BASE_DIR = Path().cwd()
# Archivo de configuraciones de cliente
CONFIG_FILE = Path(BASE_DIR / "config.ini")

PATH_DBF = get_config_setting(CONFIG_FILE, "dbf", "path")
ENCODING = get_config_setting(CONFIG_FILE, "dbf", "encoding", "cp1252")
MY_DNS = get_config_setting(CONFIG_FILE, "dbcnx", "cnxstring")


# Main Program
@click.group()
@click.version_option(prog_name="dbf2sql", version=__version__)
def cli():
    """Convert DBF files in SQL Server tables."""


@cli.command("testdb")
def testdb():
    """Testing the relational database connection"""

    import dataset

    from sqlalchemy.exc import InterfaceError

    ini_file = click.style("config.ini", fg="yellow", bold=True)
    click.secho(f"Test db connection configured in {ini_file}", fg="bright_blue")

    db = dataset.connect(MY_DNS)
    db.begin()
    try:
        click.secho("DB connection successfully!!!", fg="green", bold=True)
        db.commit()
    except (InterfaceError):
        click.secho("DB connection Error", fg="bright_red", bold=True)
        db.rollback()
    finally:
        db.close()


@cli.command("config")
@click.option(
    "--init", "-i", is_flag=True, help="Create a basic config.ini file in the current directory."
)
@click.option("--list", "-l", "list_", is_flag=True, help="List configuration settings.")
def config(init, list_):
    """
    Manages configurations settings
    """
    if init:
        if not Path(CONFIG_FILE).exists():
            create_config_file(CONFIG_FILE)

        list_config_setting(CONFIG_FILE)

    elif list_:
        list_config_setting(CONFIG_FILE)


@cli.command("convert")
@click.argument("filename", nargs=1)
@click.argument("key", nargs=1)
def convert(filename, key):
    """Convert DBF file to SQL table"""

    import dataset

    from dbfread import DBF
    from dbfread import DBFNotFound

    if PATH_DBF is None:
        raise Exception("<`-´> Ouch! Path to DBF files not found! Check it!")

    if MY_DNS is None:
        raise Exception("<`-´> Ouch! Data Source Name not exists!")

    try:
        dbf = DBF(PATH_DBF + filename, encoding=ENCODING)
        sql_tablename = PurePosixPath(filename).stem
    except DBFNotFound:
        click.echo("<`-´> Ouch! DBF File Not Found. Check path in config.ini")

    db = dataset.connect(MY_DNS)
    db.begin()
    try:
        table = db.get_table(sql_tablename)

        if isinstance(key, str):
            table.drop()
        with click.progressbar(dbf, length=len(dbf)) as dbf_rows:
            for row in dbf_rows:
                if isinstance(key, str):
                    table.insert(row)
                else:
                    table.upsert(row, key)
        db.commit()
    except (IOError, OSError):
        db.rollback()
    finally:
        db.close()
        click.echo(f"<°o°> Hooray! {sql_tablename} has been updated succesfully!")


# @cli.command("execute")
# @click.argument("query", nargs=1, type=click.STRING)
# def execute(query):
#     """Execute a custom SQL query"""
#     click.echo(query)
