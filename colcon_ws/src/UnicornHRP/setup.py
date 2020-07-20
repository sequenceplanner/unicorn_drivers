from setuptools import setup

package_name = 'UnicornHRP'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='viktor',
    maintainer_email='viktor@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'UnicornHRPTest_function = UnicornHRP.UnicornHRPTest_function:main',
        	'UnicornHRPSTOP_function = UnicornHRP.UnicornHRPSTOP_function:main',
        	'UnicornHRPTrack_function = UnicornHRP.UnicornHRPTrack_function:main',
	    ],
    },
)