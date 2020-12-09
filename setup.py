import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="e621-downloader-Hunter-The-Furry ", # Replace with your own username
    version="0.0.1",
    author="Hunter-The-Furry",
    author_email="huntertheprotogen@gmail.com",
    description="An application to download images from E621/e926",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hunter-The-Furry/e621-downloader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)