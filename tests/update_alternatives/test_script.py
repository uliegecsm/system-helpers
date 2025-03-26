import pathlib
import unittest.mock

import pytest
import pytest_console_scripts
import typeguard

class TestUpdateAlternatives:
    """
    Test :py:func:`system_helpers.update_alternatives.alternatives.update_alternatives`.
    """
    @staticmethod
    @typeguard.typechecked
    def get_script():
        """
        Retrieve script path.
        """
        return pathlib.Path(__file__).parent.parent.parent / 'system_helpers' / 'update_alternatives' / 'script.py'

    @unittest.mock.patch(target = 'subprocess.check_call', side_effect = 6 * [None])
    @pytest.mark.script_launch_mode('inprocess')
    def test_many_alternatives_in_script_mode(self, mocker, script_runner : pytest_console_scripts.ScriptRunner):
        """
        Test for a provided list of alternatives.
        """
        result = script_runner.run([
            str(self.get_script()),
            '--for-each-of',
            'gcc=gcc-10',
            'g++=g++-10',
            'python=python-3.12',
        ], print_result = True)

        assert result.returncode == 0

        mocker.assert_has_calls(calls = [
            unittest.mock.call(['update-alternatives', '--install', pathlib.Path('/usr/bin/gcc'), 'gcc', pathlib.Path('/usr/bin/gcc-10'), '10']),
            unittest.mock.call(['update-alternatives', '--display', 'gcc']),
            unittest.mock.call(['update-alternatives', '--install', pathlib.Path('/usr/bin/g++'), 'g++', pathlib.Path('/usr/bin/g++-10'), '10']),
            unittest.mock.call(['update-alternatives', '--display', 'g++']),
            unittest.mock.call(['update-alternatives', '--install', pathlib.Path('/usr/bin/python'), 'python', pathlib.Path('/usr/bin/python-3.12'), '10']),
            unittest.mock.call(['update-alternatives', '--display', 'python']),
        ])
