from setuptools import setup, find_packages

setup(
    name="py2java_translator",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask>=2.3.3',
        'flask-cors>=4.0.0',
        'gunicorn>=21.2.0',
        'pygments>=2.16.1',
        'astroid>=2.15.0',
    ],
) 