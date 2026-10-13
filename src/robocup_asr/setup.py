"""Package the reconstructed 2026 robocup_asr node."""
import os
from setuptools import find_packages, setup

package_name = 'robocup_asr'


def model_data_files():
    """Install every Vosk asset while preserving its relative directory."""
    entries = []
    for parent, _, names in os.walk('vosk_models'):
        if names:
            entries.append((os.path.join('share', package_name, parent),
                            [os.path.join(parent, name) for name in names]))
    return entries


setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ] + model_data_files(),
    install_requires=['setuptools', 'numpy==2.2.6', 'sounddevice==0.5.6', 'vosk==0.3.45'],
    zip_safe=False,
    maintainer='RoboCup voice maintainers',
    maintainer_email='maintainers@example.invalid',
    description='Offline English ASR using Vosk.',
    license='MIT',
    extras_require={'test': ['pytest>=8,<9']},
    entry_points={'console_scripts': ['vosk_asr_node = robocup_asr.vosk_asr_node:main']},
)
