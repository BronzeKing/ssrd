# -*- coding:utf-8 -*-
import argparse
import os

import importlib

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('path', help=u'方法指向的路径， 如 foo.bar  即 foo文件的bar函数')
parser.add_argument('args', nargs='*', help=u'函数的参数', default='')
parser = parser.parse_args()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')


def import_module(dotted_path):
    module_parts = dotted_path.split('.')
    if len(module_parts) < 2:
        module_parts.append('main')  # 默认调用main函数
    if len(module_parts) == 2:
        module_parts.insert(0, 'utility')  # 默认调用utility/下的文件
    module_path = ".".join(module_parts[:-1])
    module = importlib.import_module(module_path)
    return getattr(module, module_parts[-1])


def main():
    path, args = parser.path, parser.args or []
    if not os.environ.get('VIRTUAL_ENV'):
        print('\n没有进入虚拟环境\n')
    if 'server' not in path:
        try:
            from django import setup
            setup()
        except ImportError:
            pass
    func = import_module(path)
    func(*args)


if __name__ == "__main__":
    main()
