from pytest_mock import MockerFixture
from pytest import fixture


@fixture(autouse=True, scope='function')
def _suppress_logs(mocker: MockerFixture) -> None:
    """Globally suppress logger output for all tests in this module"""
    mocker.patch("docucraft.src.docx_creater.logger.warning")
