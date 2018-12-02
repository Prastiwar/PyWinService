import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WinService",
    version="0.0.1",
    author="Tomasz Piowczyk",
    author_email="tomasz.piowczyk@gmail.com",
    description="Package to manage windows service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Prastiwar/PyWinService",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)