import argparse
import shutil
import pathlib
import os
import datetime
import sys
from .version import PROJECT, get_version
from jinja2 import Environment, FileSystemLoader


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


vscode_ide_name = 'vscode'


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version',
                        action='version',
                        version=f'{PROJECT} {get_version()}')
    parser.add_argument(
        '-i',
        '--ide',
        choices=[vscode_ide_name],
        default=vscode_ide_name)
    parser.add_argument('type', choices=['app', 'lib'])
    parser.add_argument('dir', type=str)
    return parser


def render(env, input_file, output_file_dir, **kwargs):
    template_name = input_file.name
    output_file_path = output_file_dir.joinpath(
        template_name.rsplit('.', 1)[0])
    template = env.get_template(str(input_file))
    output_from_parsed_template = template.render(kwargs)
    with output_file_path.open('w') as f:
        f.write(output_from_parsed_template)


def main():
    args = arg_parser().parse_args()

    output_file_dir = pathlib.Path(args.dir)
    if output_file_dir.exists() and len(list(output_file_dir.glob('**/*'))) != 0:
        raise Exception(f'directory: {output_file_dir} is NOT EMPTY!')
    output_file_dir.mkdir(parents=True, exist_ok=True)

    templates_path = pathlib.Path(__file__).parents[0].joinpath('templates')
    env = Environment(loader=FileSystemLoader(templates_path))
    env_path = templates_path.joinpath(args.type)

    default_python_ver = f'{sys.version_info.major}.{sys.version_info.minor}'
    default_project = f'my{args.type}'
    default_author = os.environ['USER'] if 'USER' in os.environ else 'me'
    default_author_mail = f'{default_author}@outlook.com'
    default_github_url = 'https://github.com'
    default_version = '0.0.1'

    project_ = input(f'Project name[{default_project}]:') or default_project
    author_ = input(f'author[{default_author}]:') or default_author
    author_mail_ = input(
        f'mail[{default_author_mail}]:') or default_author_mail
    github_url_ = input(
        f'github url[{default_github_url}]:') or default_github_url
    python_ver_ = input(
        f'Python version[{default_python_ver}]:') or default_python_ver
    version_ = input(f'version[{default_version}]:') or default_version
    project_description_ = input('description[""]:') or ''

    if args.ide == vscode_ide_name:
        shutil.copytree(templates_path.joinpath(vscode_ide_name),
                        output_file_dir.joinpath(f'.{vscode_ide_name}'))

    template_file_name = pathlib.Path('LICENSE.jinja2')
    now = datetime.datetime.now()
    render(env,
           template_file_name,
           output_file_dir,
           author=author_,
           year=now.year)

    for f in templates_path.glob('requirements*.txt'):
        shutil.copy(f, output_file_dir)

    type_path = pathlib.Path(args.type)
    template_file_name = type_path.joinpath('Makefile.jinja2')
    render(env,
           template_file_name,
           output_file_dir,
           python_ver=python_ver_,
           project=project_)

    template_file_name = type_path.joinpath('setup.py.jinja2')
    render(env,
           template_file_name,
           output_file_dir,
           python_ver=python_ver_,
           project=project_,
           github_url=github_url_)

    template_file_name = type_path.joinpath('README.md.jinja2')
    render(env,
           template_file_name,
           output_file_dir,
           project=project_,
           version=version_,
           project_description=project_description_)

    template_file_name = pathlib.Path('Dockerfile-dev.jinja2')
    render(env, template_file_name, output_file_dir)

    template_file_name = type_path.joinpath('Dockerfile.jinja2')
    if templates_path.joinpath(template_file_name).exists():
        render(env, template_file_name, output_file_dir, project=project_)

    template_file_name = type_path.joinpath('docker-compose.yml.jinja2')
    render(env, template_file_name, output_file_dir, project=project_)

    output_file_dir = pathlib.Path(args.dir).joinpath(project_)
    output_file_dir.mkdir(parents=True, exist_ok=True)

    template_file_name = pathlib.Path('version.py.jinja2')
    ver_list = []
    for value in version_.split('.'):
        value = (int(value)) if is_int(value) else value
        ver_list.append(value)
    render(env,
           template_file_name,
           output_file_dir,
           project=project_,
           version_as_tuple=tuple(ver_list))

    init_file_name = '__init__.py'
    pathlib.Path(output_file_dir.joinpath(init_file_name)).touch()

    template_file_name = type_path.joinpath('main.py.jinja2')
    if templates_path.joinpath(template_file_name).exists():
        render(env, template_file_name, output_file_dir)

    output_file_dir = pathlib.Path(args.dir).joinpath('tests')
    output_file_dir.mkdir(parents=True, exist_ok=True)

    template_file_name = pathlib.Path('test_simple.py.jinja2')
    render(env,
           template_file_name,
           output_file_dir,
           project=project_,
           version=version_)
    pathlib.Path(output_file_dir.joinpath(init_file_name)).touch()


if __name__ == '__main__':
    main()
