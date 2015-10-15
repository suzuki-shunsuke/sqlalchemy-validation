from setuptools import setup, find_packages


setup(
    name="sqlalchemy_validation",
    version="0.2.0a0",
    packages=["sqlalchemy_validation"],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=["sqlalchemy"],
    extras_require={
        "email": ["validate_email"]
    },
    zip_safe=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst", "*.md"]
    },

    author="Suzuki Shunsuke",
    author_email="suzuki.shunsuke.1989@gmail.com",
    description=("This library supports validations based on the model class's"
                 " definition."),
    license="MIT",
    keywords="validation sqlalchemy",
    url="https://github.com/minimum-core/sqlalchemy-validation",

    # could also include long_description, download_url, classifiers, etc.
)
