from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'serial_demo'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Install launch files so `ros2 launch serial_demo ...` can find them.
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='meewoan',
    maintainer_email='meewoan@gmail.com',
    description='Demo package: read servo angle from terminal, publish it, and forward it over serial to an Arduino',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'input_publisher = serial_demo.input_publisher:main',
            'serial_bridge = serial_demo.serial_bridge:main',
        ],
    },
)
