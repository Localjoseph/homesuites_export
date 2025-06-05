from setuptools import setup, find_packages

setup(
    name="homesuites",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "django>=4.2.0",
        "django-crispy-forms>=2.0",
        "django-widget-tweaks>=1.4.12",
        "pillow>=9.5.0",
    ],
    description="Airbnb-style rental management website",
    author="Your Name",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)