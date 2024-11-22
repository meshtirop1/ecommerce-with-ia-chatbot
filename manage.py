#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django.utils.autoreload
from pathlib import Path


def fix_django_autoreload():
    original_iter_all_python_module_files = django.utils.autoreload.iter_all_python_module_files

    def iter_all_python_module_files():
        for file_path in original_iter_all_python_module_files():
            # Ensure file_path is a Path object
            if isinstance(file_path, str):
                file_path = Path(file_path)

            # Skip filenames that start and end with '<' and '>'
            if file_path.name.startswith('<') and file_path.name.endswith('>'):
                continue
            yield file_path

    django.utils.autoreload.iter_all_python_module_files = iter_all_python_module_files


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    try:
        fix_django_autoreload()  # Apply the fix before execute_from_command_line
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
