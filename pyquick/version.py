from packaging.version import Version
VERSION = (0, 0, 1, 'alpha', 4)
PROJECT = 'pyquick'


def get_version():
    return str(Version('.'.join([str(x) for x in VERSION])))
