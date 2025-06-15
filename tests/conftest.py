from pytest import fixture, LogCaptureFixture

import logging


@fixture(autouse=True)
def test(caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.CRITICAL)
