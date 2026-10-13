from setuptools import find_packages, setup

package_name = 'robocup_speech_one'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='raffiki',
    maintainer_email='raffiki@todo.todo',
    description='Bridge node: voice command → navigation + object recognition',
    license='TODO: License declaration',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'speech_one = robocup_speech_one.speech_one:main',
        ],
    },
)
