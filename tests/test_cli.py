"""Tests for the initial CLI boundary."""

import pytest

from cdd.cli import main


def test_help_exits_successfully(capsys: pytest.CaptureFixture[str]) -> None:
    """The CLI exposes its initial help screen."""
    with pytest.raises(SystemExit) as result:
        main(["--help"])

    assert result.value.code == 0
    assert "Coffee-Driven Development" in capsys.readouterr().out
