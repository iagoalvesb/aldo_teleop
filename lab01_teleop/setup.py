from setuptools import find_packages, setup

package_name = 'teleop_aldo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='iago',
    maintainer_email='iagoalves@discente.ufg.br',
    description='Atividade 1: teleop turtebot - primeiros passos',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'teleop_aldo = teleop_aldo.teleop_aldo:main'
        ],
    },
)
