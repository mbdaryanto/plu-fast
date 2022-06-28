from pathlib import Path


def get_version() -> str:
    version_file = Path(__file__).parent / 'VERSION.txt'
    with version_file.open('rt') as f:
        return f.read().strip()


def get_program_name() -> str:
    return 'PLU Webapp ver {}'.format(get_version())
