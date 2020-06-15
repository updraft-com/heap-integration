from setuptools import setup

setup(name='heaptools',
      version='0.1',
      description='Shared tools for heap server integration',
      url='https://github.com/updraft-com/heap-integration',
      author='Matt Millar',
      author_email='matt.millar@updraft.com',
      license='(C) Fairscore Ltd 2020',
      packages=['heaptools'],
      install_requires=[
          'boto3',
          'requests',
      ],
      tests_require=['pytest'],
      zip_safe=False)
