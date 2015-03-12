from setuptools import setup, find_packages

setup(
    name='oc_tools',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Boto',
    ],
    entry_points = {
            'console_scripts': [
                's3push = oc_tools.s3push:run',
            ],
        },
)


