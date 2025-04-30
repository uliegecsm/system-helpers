import pathlib
import unittest

import pytest
import pytest_console_scripts
import typeguard

from system_helpers.apt import install

class TestAptClean:
    """
    Test :py:class:`system_helpers.apt.install.Cleaner`.
    """
    @staticmethod
    @typeguard.typechecked
    def get_script():
        """
        Retrieve script path.
        """
        return pathlib.Path(__file__).parent.parent.parent / 'system_helpers' / 'apt' / 'script.py'

    def test_clean(self):
        """
        Ensure that :py:func:`system_helpers.apt.install.Cleaner.run` works as expected.
        """
        with unittest.mock.patch(target = 'subprocess.check_call', side_effect = [None]) as mocker_sp, \
             unittest.mock.patch(target = 'shutil.rmtree',         side_effect = [None]) as mocker_sh:
            install.Cleaner.run()

            mocker_sp.assert_has_calls(calls = [unittest.mock.call(['apt', 'clean'])])
            mocker_sh.assert_has_calls(calls = [unittest.mock.call(pathlib.Path('/var/lib/apt/lists'))])

    @pytest.mark.script_launch_mode('inprocess')
    def test_clean_from_cli(self, script_runner : pytest_console_scripts.ScriptRunner):
        """
        Clean `apt` using the script mode.
        """
        result = script_runner.run([
            str(self.get_script()),
            'clean',
        ], print_result = True)

        assert result.returncode == 0
