import sys
import os
import datetime

vscode_ide_name = 'vscode'


class ProjInfo:
    def __init__(self):
        self.proj_type = 'app'
        self.ide = vscode_ide_name
        self.project = f'my{self.proj_type}'
        self.python_ver = f'{sys.version_info.major}.{sys.version_info.minor}'
        self.author = os.environ['USER'] if 'USER' in os.environ else 'me'
        self.author_mail = f'{self.author}@outlook.com'
        self.github_url = 'https://github.com'
        self.version = '0.0.1'
        self.project_description = ''
        self.year = datetime.datetime.now().year

    def set_defaults(self, **kwargs):
        if 'proj_type' in kwargs:
            self.proj_type = kwargs['proj_type']
        if 'proj' in kwargs:
            self.project = kwargs['proj']
        if 'ide' in kwargs:
            self.ide = kwargs['ide']
        return self

    def get_input(self):
        self.project = input(f'Project name[{self.project}]:') or self.project
        self.author = input(f'author[{self.author}]:') or self.author
        self.author_mail = input(
            f'mail[{self.author_mail}]:') or self.author_mail
        self.github_url = input(
            f'github url[{self.github_url}]:') or self.github_url
        self.python_ver = input(
            f'Python version[{self.python_ver}]:') or self.python_ver
        self.version = input(f'version[{self.version}]:') or self.version
        self.project_description = input(
            f'description[{self.project_description}]:') or self.project_description

        return self
