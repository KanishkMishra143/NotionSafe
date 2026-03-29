import sys
import types
from unittest.mock import MagicMock, patch

import pytest

from notebackup import __main__ as app_main


def test_main_dispatches_to_qt_on_windows():
    qt_mod = types.SimpleNamespace(main=MagicMock())
    with patch("notebackup.__main__.freeze_support") as freeze_mock:
        with patch("notebackup.__main__.platform.system", return_value="Windows"):
            with patch.dict(sys.modules, {"notebackup.ui.qt_ui": qt_mod}, clear=False):
                app_main.main()

    freeze_mock.assert_called_once()
    qt_mod.main.assert_called_once()


def test_main_dispatches_to_gtk_on_linux():
    gtk_mod = types.SimpleNamespace(main=MagicMock())
    with patch("notebackup.__main__.freeze_support") as freeze_mock:
        with patch("notebackup.__main__.platform.system", return_value="Linux"):
            with patch.dict(sys.modules, {"notebackup.ui.gtk_ui": gtk_mod}, clear=False):
                app_main.main()

    freeze_mock.assert_called_once()
    gtk_mod.main.assert_called_once()


def test_main_exits_for_unsupported_platform():
    with patch("notebackup.__main__.freeze_support"):
        with patch("notebackup.__main__.platform.system", return_value="Darwin"):
            with pytest.raises(SystemExit) as exc_info:
                app_main.main()

    assert exc_info.value.code == 1
