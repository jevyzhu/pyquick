from setuptools import setup, find_packages

project="pyquick"
python_ver="3.8"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=project,
    version="0.0.1.1a0",
    author="jingwei zhu",
    author_email="jingweizhucn@126.com",
    description="A Python Demo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/jevyzhu/{project}",
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    include_package_data=True,
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
