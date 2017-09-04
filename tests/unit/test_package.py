"""Package related tests."""


def test_import():
    """Test import."""
    import shortmagnet  # noqa


def test_options():
    """Test options are called."""
    import shortmagnet
    import sys
    sys.argv = [sys.argv[0]]
    assert shortmagnet.main() == {}
