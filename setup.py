from setuptools import setup, find_packages

setup(
	name='project3',
	version='1.0',
	author='Manoj Virinchi',
	author_email='mchitta@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)