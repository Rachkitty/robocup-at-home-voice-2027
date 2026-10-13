"""Package the reconstructed 2026 robocup_tts node."""
from setuptools import find_packages, setup

package_name = 'robocup_tts'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'numpy==2.2.6', 'piper-tts==1.4.2', 'sounddevice==0.5.6'],
    zip_safe=False,
    maintainer='RoboCup voice maintainers',
    maintainer_email='maintainers@example.invalid',
    description='Offline speech synthesis using a user-provided Piper voice.',
    license='MIT',
    extras_require={'test': ['pytest>=8,<9']},
    entry_points={'console_scripts': ['tts_node = robocup_tts.tts_node:main']},
)
