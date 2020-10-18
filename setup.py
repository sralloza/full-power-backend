from setuptools import setup

import versioneer

setup(
    name="heath-bot-backend",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
