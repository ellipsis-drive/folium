import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="foliumEllipsis",
    version="0.0.0",
    author="Daniel van der Maas",
    author_email="daniel@ellipsis-drive.com",
    description="Package to add Ellipsis Drive layers to folium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ellipsis-drive/folium",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
    'folium',
    'folium_vectortilelayer',
    'json',
    'requests',
    'uuid'
    ],
    python_requires='>=3.6',
)
