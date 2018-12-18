from setuptools import setup

setup(
    name="pythonCommunicator",
    version="0.1.0",
    author="Andres Anania",
    author_email="aanania@lsst.org",
    description="Package to manage TCP and Serial communication",
    url="https://github.com/lsst-ts/pythonCommunicator",
    install_requires=["asyncio","pySerial"],
    packages=["lsst.ts.pythonCommunicator"],
    package_dir={"":"python"}
)
