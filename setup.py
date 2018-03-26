

#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

setup(name = 'stats',
      description = 'Package for playing with writing statistical methods.',
      author = 'C.M. Gosmeyer',
      url = 'https://github.com/cgosmeyer/learning_statistics',
      packages = find_packages(),
      install_requires = ['numpy'],
      #package_data = {'stats' : ['stats/tables/*.csv']},
      include_package_data=True
     )

