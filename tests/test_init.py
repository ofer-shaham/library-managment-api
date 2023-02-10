from flaskr import create_app
from flaskr.library.models import *


def test_config():
    """Test create_app without passing test config."""
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_db_url_environ(monkeypatch):
    """Test DATABASE_URL environment variable."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///environ")
    app = create_app()
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///environ"


def test_init_db_command(runner, monkeypatch):
    called = False

    def fake_init_db():
        nonlocal called
        called = True

    monkeypatch.setattr("flaskr.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert called


def test_mock_variable_value(monkeypatch):
    # mocked return constant to ease testing

    monkeypatch.setattr("flaskr.utils.constants.MAX_CHECKED_OUT", 1)
    from flaskr.utils.constants import MAX_CHECKED_OUT
    assert MAX_CHECKED_OUT == 1
