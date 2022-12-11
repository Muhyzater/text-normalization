from setuptools import find_packages, setup

setup(
    name="Text Normalization",
    version="v4.1.10",
    description="Perform Text Normalization",
    author="",
    author_email="",
    license="Proprietary: Mawdoo3 internal use only",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Natural Language :: Arabic",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords="mawdoo3 NLP Text Normalization",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=[
        "antlr4-python3-runtime==4.7.2",
        "pyarabic==0.6.10",
        "phonenumbers",
        "matplotlib",
        "grpcio",
        "grpcio-health-checking==1.29",
        "grpcio-reflection==1.29",
    ],
    test_suite="nose2.collector.collector",
    extras_require={
        "test": ["nose2"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "mawdoo3-text-normalization=text_normalization.api:text_normalization_service",
        ],
    },
)
