from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="LLMOPS-03",
    version="0.1",
    author="Bharatbhushan",
    packages=find_packages(),
    install_requires = requirements,
)