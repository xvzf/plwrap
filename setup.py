import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plwrap",
    version="0.1.0",
    author="Matthias Riegler",
    author_email="me@xvzf.tech",
    description="Non ORM SQL Query runner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xvzf/plwrap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: AsyncIO",
        "Topic :: Database",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires=">=3.6",
    install_requires=["asyncpg>=0.19.0"]
)