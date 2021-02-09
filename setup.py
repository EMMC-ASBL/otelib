import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ontotransserver-pkg-quaat", 
    version="0.0.1",
    author="Thomas F. Hagelien",
    author_email="Thomas.F.Hagelien@sintef.no",
    description="Library for represent a remote OntoTrans REST API on the network.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quaat/otserver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
