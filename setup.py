from setuptools import setup, find_packages

setup(
    name="aws",  # Package name
    version="0.1.0",    # Initial version
    author="Peter van Elsacker",
    author_email="petervanelsacker@gmail.com",
    description="Layer to simplify the use of boto3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/peer3737/aws",
    packages=find_packages(),  # Automatically find subpackages
    install_requires=[
        # List dependencies, e.g., "requests", "numpy>=1.20.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.11",  # Minimum Python version
)
