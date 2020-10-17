"""Module for package-specific tasks."""
from setuptools import setup

setup(name='gta3savedump',
      version='0.0.1',
      author='Andrew Udvare',
      author_email='audvare@gmail.com',
      py_modules=['gta3savedump'],
      url='https://github.com/Tatsh/gta3savedump',
      license='LICENSE.txt',
      description='Dumps a GTA 3 save file into a readable representation.',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      python_requires='>=3.8',
      classifiers=['Topic :: Utilities'],
      entry_points={
          'console_scripts': [
              'gta3savedump = gta3savedump:command',
          ]
      })
