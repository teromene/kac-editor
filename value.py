#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os
try:
    import py2exe
    import py2exe.build_exe
    import py2exe.build_exe.isSystemDLL
except ImportError:
    pass
else:
    origIsSystemDLL = py2exe.build_exe.isSystemDLL

    def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in {
            "libfreetype-6.dll",
            "sdl_ttf.dll",
            "libogg-0.dll",
        }:
            return 0
        return origIsSystemDLL(pathname)

    py2exe.build_exe.isSystemDLL = isSystemDLL


setup(
    name='pyfile.exe',
    version='1.1',
    description='A binary launcher for PyGame.',
    scripts=['runner.py'],
    py_modules=['runner'],
    zip_safe=True,
    install_requires=['distribute', 'pygame'],
    keywords='pygame windows launcher',
    options = {
        'py2exe': {
            'bundle_files': 1,
            'compressed': True,
            'excludes': [
                'doctest',
                'pdb',
                'unittest',
                'difflib',
                'inspect',
                'pyreadline',
                'email',
                '_ssl',
            ]
        },
    },
    windows = [
        {
            'script': "runner.py",
            'icon_resources': [(0, "pygame.ico")],
        }
    ],
    zipfile = None,
    classifiers=[
        "Classifier: Development Status :: 5 - Production/Stable",
        "Classifier: Environment :: Win32 (MS Windows)",
        "Classifier: Intended Audience :: End Users/Desktop",
        "Classifier: License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Classifier: Operating System :: Microsoft :: Windows",
        "Classifier: Programming Language :: Python",
        "Classifier: Programming Language :: Python :: 2.7",
        "Classifier: Topic :: Games/Entertainment",
        "Classifier: Topic :: Multimedia",
        "Classifier: Topic :: Software Development :: Build Tools",
        "Classifier: Topic :: System :: Installation/Setup",
        "Classifier: Topic :: System :: Software Distribution",
        "Classifier: Topic :: Utilities",
    ],
)
