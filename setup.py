import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crappytdms",
    version="0.0.1",
    author="Leberwurscht",
    author_email="leberwurscht@hoegners.de",
    description="A crappy library for efficiently reading large TDMS files with and without index files, based on pyTDMS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/leberwurscht/crappytdms",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pytdms'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3'
)
