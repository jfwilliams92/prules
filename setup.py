import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prules", # Replace with your own username
    version="0.0.1",
    author="James Williams",
    author_email="jfw@g.clemson.edu",
    description="A package for evaluation of Json backed rules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jfwilliams92/prules",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)