import pathlib
import unittest

import pytest
import pytest_console_scripts
import typeguard

from system_helpers.apt import extract

class TestAptExtract:
    """
    Test functionalities of :py:mod:`system_helpers.apt.extract`.
    """
    APT_POLICY_CCACHE = \
"""
ccache:
  Installed: (none)
  Candidate: 4.8+really4.7.5-1
  Version table:
     4.8+really4.7.5-1 500
        500 http://deb.debian.org/debian bookworm/main amd64 Packages
"""
    @staticmethod
    @typeguard.typechecked
    def get_script():
        """
        Retrieve script path.
        """
        return pathlib.Path(__file__).parent.parent.parent / 'system_helpers' / 'apt' / 'script.py'

    def test_candidate(self):
        """
        Ensure that :py:func:`system_helpers.apt.extract.candidate` works as expected.
        """
        with unittest.mock.patch(target = 'subprocess.check_output', side_effect = [self.APT_POLICY_CCACHE.encode()]) as mocker:
            assert extract.candidate(package = 'ccache') == "4.8%2breally4.7.5-1"

            mocker.assert_has_calls(calls = [unittest.mock.call(['apt', 'policy', 'ccache'])])

    def test_extract_single_file(self):
        """
        Try to extract and install a single file from the `jq` package.
        """
        extract.extract(package = 'jq', files = ['./usr/bin/jq'])

        assert pathlib.Path('/usr/bin/jq').is_file()

    def test_extract_many_files(self):
        """
        Try to extract and install many files from the `jq` package.
        """
        extract.extract(package = 'jq', files = ['./usr/bin/jq', './usr/share/doc/jq'])

        assert pathlib.Path('/usr/bin/jq').is_file()
        assert pathlib.Path('/usr/share/doc/jq/README').is_file()

    @pytest.mark.script_launch_mode('inprocess')
    def test_install_packages_from_cli(self, script_runner : pytest_console_scripts.ScriptRunner):
        """
        Install files from the `ccache` package using the script mode.
        """
        result = script_runner.run([
            str(self.get_script()),
            'extract-from-package',
            '--package', 'ccache',
            '--files', './usr/bin/ccache',
        ], print_result = True)

        assert result.returncode == 0

        assert pathlib.Path('/usr/bin/ccache').is_file()

    @pytest.mark.script_launch_mode('inprocess')
    def test_install_packages_from_cli(self, script_runner : pytest_console_scripts.ScriptRunner):
        """
        Install files from the `llvm` package using the script mode.
        """
        result = script_runner.run([
            str(self.get_script()),
            'extract-from-package',
            '--package', 'llvm',
            '--files', './usr/bin/llvm-cxxfilt', './usr/bin/llvm-split',
        ], print_result = True)

        assert result.returncode == 0

        assert pathlib.Path('/usr/bin/llvm-cxxfilt').is_symlink()
        assert pathlib.Path('/usr/bin/llvm-split').is_symlink()
