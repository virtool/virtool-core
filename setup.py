import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="virtool-core",
    version="0.0.1",
    description="core utilities for Virtool backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/virtool/virtool-core",
    packages=setuptools.find_packages(),
    python_requires=">=3.6"
)
