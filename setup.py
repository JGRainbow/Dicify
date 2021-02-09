import distutils.cmd
import distutils.log
import setuptools
import subprocess
import shutil

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fp:
    install_requires = fp.read()

setuptools.setup(
    name="dicify",
    version="0.0.0",
    author="Jacob Rainbow",
    author_email="jacob.rainbow@gmail.com",
    description="a short description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JGRainbow/Dicify",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=True
)