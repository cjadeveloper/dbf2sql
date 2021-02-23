from pathlib import Path

from dbf2sql.__version__ import __version__


def test_version():
    assert __version__ == "0.1.1-dev1"


def test_config_file(monkeypatch):
    # given
    def mock_config_file():
        return Path("/configdir") / "config.ini"

    monkeypatch.setattr(Path, "cwd", mock_config_file)

    # when
    config_file_path = Path.cwd()

    # then
    assert config_file_path == Path("/configdir/config.ini")
