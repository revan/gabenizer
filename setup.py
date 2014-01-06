from setuptools import setup

setup(name='gabenizer',
      version='1.0',
      description='OpenShift App',
      author='Revan Sopher',
      author_email='rsopher@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask>=0.7.2', 'MarkupSafe', 'praw', 'unirest', 'Pillow'],
     )
