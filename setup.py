# setup.py
from setuptools import setup, find_packages

setup(
    name="imclib",
    version="0.1",
    packages=find_packages(),
    description="Librería para cálculo y gestión de IMC en CSV",
    author="Ander Villar",
    install_requires=[
        "pandas"
    ],
    python_requires=">=3.8"
)