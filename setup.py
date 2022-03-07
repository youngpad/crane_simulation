from setuptools import setup

package_name = 'crane_simulator'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Martin Maeland',
    maintainer_email='martinmaeland@outlook.com',
    description='Crane simulator for MAS418.',
    license='license',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simulator = crane_simulator.simulator:main',
        ],
    },
)
