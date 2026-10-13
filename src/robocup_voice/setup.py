"""Package the reconstructed 2026 robocup_voice node."""
import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'robocup_voice'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ] + [(os.path.join('share', package_name, 'config'), glob('config/*.yaml'))],
    install_requires=['setuptools', 'PyYAML==6.0.3'],
    zip_safe=False,
    maintainer='RoboCup voice maintainers',
    maintainer_email='maintainers@example.invalid',
    description='Historical keyword dialogue and confirmation state machine.',
    license='MIT',
    extras_require={'test': ['pytest>=8,<9']},
    entry_points={'console_scripts': ['voice_node = robocup_voice.voice_node:main']},
)
