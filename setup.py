"""
Setup file for the Harte Library package
"""

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="harte-library",
    version="0.3.1",
    author="Andrea Poltronieri",
    description="Library for parsing Harte chords and converting them to Music21",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    py_modules=["harte"],
    package_dir={"harte-library": "harte"},
    install_requires=["music21", "numpy", "lark"],
    package_data={"": ["*.lark"]},
    include_package_data=True,
)
