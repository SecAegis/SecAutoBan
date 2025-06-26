import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name="SecAutoBan",
    version="4.0.0",
    author="SecReport",
    author_email="secaegis@outlook.com",
    description="SecAutoBan SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SecAegis/SecAutoBan",
    packages=setuptools.find_packages(),
    install_requires = ["pycryptodome", "websocket-client", "ipaddress"]
)
