from setuptools import setup

setup(name='CommentGPT',
      version='0.2',
      description='A python module that automatically comments code with ChatGPT, uses the free/plus version online without tokens',
      url='https://github.com/brendankane04/CommentGPT',
      author='Brendan Kane',
      author_email='brendankane04@gmail.com',
      license='MIT',
      packages=['CommentGPT'],
      install_requires=['tqdm', 'difflib', 'getopt'],
      zip_safe=False)