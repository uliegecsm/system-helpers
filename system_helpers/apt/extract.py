import argparse
import logging
import pathlib
import re
import subprocess
import tempfile
import typing
import urllib.parse

import typeguard

from system_helpers.apt import install

@typeguard.typechecked
def parse_args() -> argparse.Namespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--package', type = str, required = True)
    parser.add_argument('--files',   nargs='+')

    return parser.parse_args()

@typeguard.typechecked
def candidate(*, package : str) -> str:
    """
    Get candidate version for `package`.
    """
    output = subprocess.check_output(['apt', 'policy', package]).decode()
    try:
        version = re.search(
            pattern = r'Candidate: ([a-z0-9.\-~+:]+)',
            string  = output,
        ).group(1)
    except AttributeError:
        logging.exception(output)
        raise
    return urllib.parse.quote_plus(version).lower()

@typeguard.typechecked
def extract(*, package : str, files : typing.List[str], arch : str = 'amd64', clean : bool = True) -> None:
    """
    Download `.deb` for `package` and install only the specified `files`.
    """
    logging.info(f'Extracting files {files} from package {package}.')

    install.install_packages(
        update = True,
        clean = False,
        args = ['--download-only'],
        packages = [package],
    )

    version = candidate(package = package)

    logging.info(f'Candidate version for {package} is {version}.')

    deb = pathlib.Path('/var/cache/apt/archives/') / f'{package}_{version}_{arch}.deb'

    if not deb.is_file():
        raise FileNotFoundError(deb)

    with tempfile.TemporaryDirectory() as tmpdir:
        # List files in the archive. We'll look for the data part.
        cmd = ['ar', 'tv', deb]
        content = re.search(
            pattern = r'(data\.[a-z\.]+)',
            string  = subprocess.check_output(cmd, cwd = tmpdir).decode(),
        ).group(1)

        cmd = ['ar', 'xv', deb, '--output=' + tmpdir]

        logging.info(f'Opening {deb} with {cmd}.')

        subprocess.check_call(cmd, cwd = tmpdir)

        data = pathlib.Path(tmpdir) / content

        if not data.is_file():
            raise FileNotFoundError(data)

        cmd = ['tar', '-C', '/', '-xvf', data, *files]

        logging.info(f'Extracting files with {cmd}.')

        subprocess.check_call(cmd, cwd = tmpdir)

    if clean: install.Cleaner.run()

if __name__ == '__main__':

    logging.basicConfig(level = logging.INFO)

    args = parse_args()

    logging.info(f"Received arguments: {args}")

    extract(**vars(args))
