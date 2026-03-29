import sys
from unittest.mock import patch

from cleo.io.outputs.stream_output import StreamOutput

from notebackup.exporter import export_cli


def test_export_cli_invokes_notion2md_with_download_flag_and_restores_globals():
    original_argv = sys.argv
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    original_color_support = StreamOutput._has_color_support
    captured = {}

    def fake_main():
        captured["argv"] = list(sys.argv)
        print("ok")
        return 0

    with patch("notebackup.exporter.notion2md_main", side_effect=fake_main):
        exit_code = export_cli(["--token", "dummy_token", "--id", "dummy_id"])

    assert exit_code == 0
    assert captured["argv"][0] == "notion2md"
    assert "--download" in captured["argv"]
    assert sys.argv is original_argv
    assert sys.stdout is original_stdout
    assert sys.stderr is original_stderr
    assert StreamOutput._has_color_support is original_color_support


def test_export_cli_returns_one_when_notion2md_raises():
    with patch("notebackup.exporter.notion2md_main", side_effect=RuntimeError("boom")):
        exit_code = export_cli(["--token", "dummy_token"])

    assert exit_code == 1
