import psycopg2
import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(psycopg2.InterfaceError) as e:
        with db.cursor() as cursor:
            cursor.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    """Note: テストしたいのは「コマンドが呼ばれるかどうか」であって
    DB の初期化までは意図していない？
    そのため DB の初期化はフェイクにしている？
    """
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
