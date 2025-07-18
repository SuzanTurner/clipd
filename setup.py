from setuptools import setup, find_packages

setup(
    name="clipd",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "clipd = clipd.main:main"
        ]
    },
)
