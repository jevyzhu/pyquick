import pathlib
from setuptools import setup, find_packages
from pyquick.version import get_version, PROJECT
import pkg_resources

python_ver = "3.7"
project = PROJECT

with open("README.md", "r") as fh:
    long_description = fh.read()

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name=project,
    version=get_version(),
    author="jingwei zhu",
    author_email="jingweizhucn@126.com",
    description="A Python Demo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/jevyzhu/{project}",
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=f">={python_ver}",
    entry_points="""
        [console_scripts]
        pyquick = pyquick.main:main
    """,
)
