import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paywix",
    version="3.0.0",
    author="Renjith S Raj",
    author_email="renjithsraj@live.com",
    description="Multi payment gateway wrapper for Django based applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/renjithsraj/paywix",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
