import shutil
import pathlib
from jinja2 import Environment, FileSystemLoader
from .proj import ProjInfo, vscode_ide_name
from .args import arg_parser


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def render(env, input_file, output_file_dir, **kwargs):
    template_name = input_file.name
    output_file_path = output_file_dir.joinpath(
        template_name.rsplit('.', 1)[0])
    template = env.get_template(str(input_file))
    output_from_parsed_template = template.render(kwargs)
    with output_file_path.open('w') as f:
        f.write(output_from_parsed_template)


def generate_proj(templates_path: pathlib.Path,
                  target_dir: pathlib.Path,
                  proj_info: ProjInfo):
    output_file_dir = target_dir
    env = Environment(loader=FileSystemLoader(templates_path))

    if proj_info.ide == vscode_ide_name:
        shutil.copytree(templates_path.joinpath(vscode_ide_name),
                        output_file_dir.joinpath(f'.{vscode_ide_name}'))

    shutil.copy(templates_path.joinpath('gitignore'),
                output_file_dir.joinpath('.gitignore'))

    template_file_name = pathlib.Path('LICENSE.jinja2')
    render(env,
           template_file_name,
           output_file_dir,
           author=proj_info.author,
           year=proj_info.year)

    for f in templates_path.glob('requirements*.txt'):
        shutil.copy(f, output_file_dir)

    type_path = pathlib.Path(proj_info.proj_type)
    template_file_name = type_path.joinpath('Makefile.jinja2')
    render(env,
           template_file_name,
           output_file_dir,
           python_ver=proj_info.python_ver,
           project=proj_info.project)

    template_file_name = type_path.joinpath('setup.py.jinja2')
    render(env,
           template_file_name,
           output_file_dir,
           python_ver=proj_info.python_ver,
           project=proj_info.project,
           github_url=proj_info.github_url)

    template_file_name = type_path.joinpath('README.md.jinja2')
    render(env,
           template_file_name,
           output_file_dir,
           project=proj_info.project,
           version=proj_info.version,
           project_description=proj_info.project_description)

    template_file_name = pathlib.Path('Dockerfile-dev.jinja2')
    render(env, template_file_name, output_file_dir)

    template_file_name = type_path.joinpath('Dockerfile.jinja2')
    if templates_path.joinpath(template_file_name).exists():
        render(
            env,
            template_file_name,
            output_file_dir,
            project=proj_info.project)

    template_file_name = type_path.joinpath('docker-compose.yml.jinja2')
    render(env, template_file_name, output_file_dir, project=proj_info.project)

    output_file_dir = target_dir.joinpath(proj_info.project)
    output_file_dir.mkdir(parents=True, exist_ok=True)

    template_file_name = pathlib.Path('version.py.jinja2')
    ver_list = []
    for value in proj_info.version.split('.'):
        value = (int(value)) if is_int(value) else value
        ver_list.append(value)
    render(env,
           template_file_name,
           output_file_dir,
           project=proj_info.project,
           version_as_tuple=tuple(ver_list))

    init_file_name = '__init__.py'
    pathlib.Path(output_file_dir.joinpath(init_file_name)).touch()

    template_file_name = type_path.joinpath('main.py.jinja2')
    if templates_path.joinpath(template_file_name).exists():
        render(env, template_file_name, output_file_dir)

    output_file_dir = target_dir.joinpath('tests')
    output_file_dir.mkdir(parents=True, exist_ok=True)

    template_file_name = pathlib.Path('test_simple.py.jinja2')
    render(env,
           template_file_name,
           output_file_dir,
           project=proj_info.project,
           version=proj_info.version)
    pathlib.Path(output_file_dir.joinpath(init_file_name)).touch()


def main():
    args = arg_parser().parse_args()
    output_file_dir = pathlib.Path(args.dir)
    if output_file_dir.exists() and len(list(output_file_dir.glob('**/*'))) != 0:
        raise Exception(f'directory: {output_file_dir} is NOT EMPTY!')
    output_file_dir.mkdir(parents=True, exist_ok=True)

    templates_path = pathlib.Path(__file__).parents[0].joinpath('templates')
    proj_info = ProjInfo().set_defaults(proj_type=args.proj_type,
                                        proj=f'my{args.proj_type}',
                                        ide=vscode_ide_name).get_input()
    generate_proj(templates_path, output_file_dir, proj_info)


if __name__ == '__main__':
    main()
