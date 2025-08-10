from setuptools import setup, find_packages

setup(
    name="ira-companion",
    version="0.1.0",
    description="Holistic AI life assistant: mental, emotional, physical, spiritual, and financial support.",
    author="Your Name or Org",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask",
        "Flask-JWT-Extended",
        "Flask-WTF",
        "SQLAlchemy",
        "gunicorn",
        "google-auth-oauthlib",
        "google-api-python-client",
        "Werkzeug",
        "pytest"
    ],
    entry_points={
        "console_scripts": [
            "ira=src:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)