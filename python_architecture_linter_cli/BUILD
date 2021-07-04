python_library(
    name="python_architecture_linter_cli",
    sources=["**/*.py"]
		)
poetry_requirements()

#python_tests(
#    name='tests',
#    sources=["**/test_*.py"
#])


python_distribution(
    name="dist-cli",
    dependencies=[ 
        ":python-architecture-linter",
        ":python_architecture_linter_cli"
    ],
    provides=setup_py(
        name="python_architecture_linter_cli",
        version="2.21.0",
        description="An example distribution built with Pants.",
        author="Pantsbuild",
        classifiers=[
            "Programming Language :: Python :: 3.7",
        ],
    ),
    setup_py_commands=["sdist", "bdist_wheel", "--python-tag", "py36.py37"]
)
