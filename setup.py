# Copyright (c) 2016 MXCHIP Limited, All Rights Reserved
# SPDX-License-Identifier: Apache-2.0

# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, 
# either express or implied.

import os
from setuptools import setup
import subprocess
import sys

LONG_DESC = open('pypi_readme.rst').read()
LICENSE = open('LICENSE').read()

setup(
    name="mico-cube",
    version="1.0.0",
    description="MXCHIP MiCO command line tool for repositories version control, publishing and updating code from remotely hosted repositories, and invoking MiCO OS own build system and export functions, among other operations",
    long_description=LONG_DESC,
    url='https://code.aliyun.com/mico/mico-cube',
    author='MXCHIP MiCO',
    author_email='yangsw@mxchip.com',
    license=LICENSE,
    packages=["mico"],
    entry_points={
        'console_scripts': [
            'mico=mico.mico:main',
            'mico-cube=mico.mico:main',
        ]
    },
)

# if windows
if sys.platform == 'win32':
    # if not register
    if subprocess.Popen('reg query "HKEY_CLASSES_ROOT\directory\shell\mico_cube" /s', stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait() == 1:
        os.system('mico-cube.reg')
