import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

INSTALL_REQUIRES = [
    "aiofiles==0.6.0",
    "arrow==0.15.5",
    "dictdiffer==0.8.1",
    "motor==2.3.0"
]

setuptools.setup(
    name="virtool_core",
    version="0.1.0",
    description="core utilities for Virtool backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/virtool/virtool-core",
    packages=[pkg for pkg in setuptools.find_packages() if "test" not in pkg],
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.6"
)
