import itertools
import pathlib
import tempfile
import typing
import unittest.mock

import pytest
import pytest_console_scripts
import typeguard

from system_helpers.apt import install

@pytest.fixture
@typeguard.typechecked
def requirements() -> typing.Generator[typing.Tuple[typing.List[pathlib.Path], typing.List[str]], None, None]:
    """
    Get requirements files *à la* `pip`.
    """
    with tempfile.NamedTemporaryFile(mode = 'w+') as req_1, \
         tempfile.NamedTemporaryFile(mode = 'w+') as req_2:
        req_1.write("# Let's start this first requirements file with a comment. Then, add some packages.\n")
        req_1.write("git\n")
        req_1.write("and\n")
        req_1.write("\n")
        req_1.write("# Some other useless comments here.\n")
        req_1.write("whatnot\n")
        req_1.flush()

        req_2.write("# Let's start this other requirements file with a comment. Then, add some packages.\n")
        req_2.write("cmake\n")
        req_2.write("is\n")
        req_2.write("nice even with many whatever\n")
        req_2.flush()

        packages = ['git', 'and', 'whatnot', 'cmake', 'is', 'nice', 'even', 'with', 'many', 'whatever']

        yield ([pathlib.Path(req_1.name), pathlib.Path(req_2.name)], packages)

class TestAptInstall:
    """
    Test :py:class:`apt_helpers.install.apt_install_packages`.
    """
    @staticmethod
    @typeguard.typechecked
    def get_script():
        """
        Retrieve script path.
        """
        return pathlib.Path(__file__).parent.parent.parent / 'system_helpers' / 'apt' / 'script.py'

    def test_list_of_package_names(self):
        """
        Test for a provided list of package names.
        """
        packages = ['git', 'and', 'whatnot']

        with unittest.mock.patch(target = 'subprocess.check_call', side_effect = [None, None]) as mocker:
            install.install_packages(packages = packages, update = False, upgrade = True, clean = False, args = ['--download-only'])

            mocker.assert_has_calls(calls = [
                unittest.mock.call(['apt', '--yes', 'upgrade']),
                unittest.mock.call(['apt', '--yes', '--no-install-recommends', 'install', '--download-only'] + packages),
            ])

    def test_list_of_requirements_files(self, requirements):
        """
        Test for a provided list of requirement files, *à la* `pip`.
        """
        with unittest.mock.patch(target = 'subprocess.check_call', side_effect = [None]) as mocker:
            install.install_packages(requirements = requirements[0], update = False, upgrade = False, clean = False)

            mocker.assert_has_calls(calls = [
                unittest.mock.call(['apt', '--yes', '--no-install-recommends', 'install'] + requirements[1]),
            ])

    @unittest.mock.patch(target = 'subprocess.check_call', side_effect = [None, None])
    @pytest.mark.script_launch_mode('inprocess')
    def test_install_packages_from_cli(self, mocker, script_runner : pytest_console_scripts.ScriptRunner, requirements):
        """
        Install many `APT` through requirement-like files and package names given to the CLI.
        """
        result = script_runner.run([
            str(self.get_script()),
            'install-packages',
            '--update',
            '--packages', 'one', 'two',
            *list(itertools.chain.from_iterable([['--requirement', str(x)] for x in requirements[0]])),
            '--args', '--download-only', '--reinstall',
        ], print_result = True)

        assert result.returncode == 0

        mocker.assert_has_calls(calls = [
            unittest.mock.call(['apt', 'update']),
            unittest.mock.call(['apt', '--yes', '--no-install-recommends', 'install', '--download-only', '--reinstall', 'one', 'two'] + requirements[1]),
        ])
