import pathlib
import shutil
import unittest
import pytest
from pyquick.main import *


class test_simple(unittest.TestCase):
    def test_0(self):
        args = arg_parser().parse_args(['-i', 'vscode', 'app', './tmp'])
        assert args.dir == './tmp'
        assert args.proj_type == 'app'
        assert args.ide == 'vscode'
        args = arg_parser().parse_args(['-i', 'vscode', 'lib', './tmp'])
        assert args.dir == './tmp'
        assert args.proj_type == 'lib'
        assert args.ide == 'vscode'
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            args = arg_parser().parse_args(['--version'])
            assert 'pyquick' in args.version

    def test_1(self):
        templates_path = pathlib.Path(
            __file__).parents[0].joinpath('../pyquick/templates')
        proj_info = ProjInfo().set_defaults(proj_type='app',
                                            proj='myapp',
                                            ide='vscode')
        output_file_dir = pathlib.Path('tmp')
        generate_proj(templates_path, output_file_dir, proj_info)
        shutil.rmtree(output_file_dir)

    def test_2(self):
        templates_path = pathlib.Path(
            __file__).parents[0].joinpath('../pyquick/templates')
        proj_info = ProjInfo().set_defaults(proj_type='lib',
                                            proj='myapp',
                                            ide='vscode')
        output_file_dir = pathlib.Path('tmp')
        generate_proj(templates_path, output_file_dir, proj_info)
        shutil.rmtree(output_file_dir)
