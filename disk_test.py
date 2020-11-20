from disk import Disk


def test_constructor():
    the_disk = Disk(100, 100, 100, "BLUE")
    # Test minimal required constructor args
    assert the_disk.rate == 25 and \
        the_disk.land is False
