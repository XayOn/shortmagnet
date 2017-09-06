"""Main tests."""


try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch


def test_create_app():
    """Test app creation and redis init."""
    import shortmagnet
    with patch('shortmagnet.FlaskRedis') as redis:
        with patch('shortmagnet.Flask') as flask:
            results = shortmagnet.create_app()
            assert len(results) == 2
            flask.assert_called_with(shortmagnet.__name__)
            redis.assert_called_with()
            redis().init_app.assert_called_with(flask())
            assert results[0] == flask()
            assert results[1] == redis()


def test_redis_config():
    """Test redis config extraction."""
    import os.path
    import sys

    config = os.path.join(os.path.dirname(__file__),
                          '../', 'fixtures', 'main.conf')

    import shortmagnet

    app, redis = MagicMock(), MagicMock()
    app.config = {}

    with patch('shortmagnet.create_app', side_effect=((app, redis,),)):
        sys.argv = [sys.argv[0], '--config', config]
        shortmagnet.main()
        assert app.config['REDIS_URL'] == "foobar"

    with patch('shortmagnet.create_app', side_effect=((app, redis,),)):
        sys.argv = [sys.argv[0]]
        shortmagnet.main()
        assert app.config['REDIS_URL'] == "redis://localhost:6379/0"


def test_main_view():
    """Test main view with fake redis."""
    import shortmagnet
    from mockredis import MockRedis

    redis = MockRedis()
    with patch('shortmagnet.request') as request:
        request.method = "POST"
        request.form = {'magnet': 'magnet:foobar'}
        result = shortmagnet.index("magnet:foobar", redis)
        assert result
        request.method = "GET"
        response = shortmagnet.index(result, redis)
        assert response.status_code == 302
        assert response.location == "magnet:foobar"


def test_main_view_assert_error():
    """Test main view with fake redis."""
    import pytest
    import shortmagnet
    from mockredis import MockRedis

    redis = MockRedis()
    with patch('shortmagnet.request') as request:
        with pytest.raises(AssertionError):
            request.method = "POST"
            request.form = {'magnet': 'foobar'}
            shortmagnet.index("foobar", redis)
