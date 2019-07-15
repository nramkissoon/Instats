import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="instats",
    version="1.0.0",
    author="Nicholas Ramkissoon",
    description="Package for processing statistics from Instagram profiles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nramkissoon/Instats",
    packages=setuptools.find_packages(),
    python_requires='>=3',
    classifiers=[
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
