from setuptools import setup

REQUIREMENTS = ['click', 'robotframework']

setup(
    name='robot_flow',
    version='0.1',
    install_requires=REQUIREMENTS,
    packages=['robot_flow'],
    entry_points={
        'console_scripts': [
            'robot_flow=robot_flow.main:cli',
        ],
    }
)