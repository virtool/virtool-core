import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="virtool_core",
    version="0.0.2",
    description="core utilities for Virtool backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/virtool/virtool-core",
    packages=[pkg for pkg in setuptools.find_packages() if "test" not in pkg],
    python_requires=">=3.6"
)
