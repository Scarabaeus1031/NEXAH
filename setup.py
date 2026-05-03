from setuptools import setup, find_packages

setup(
    name="nexah",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-learn"
    ],
    entry_points={
        "console_scripts": [
            "nexah=nexah.cli:main",
        ],
    },
)
