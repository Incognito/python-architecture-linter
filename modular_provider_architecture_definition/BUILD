python_library(
    name="modular_provider_architecture_definition",
    sources=["**/*.py"]
		)
poetry_requirements()

python_tests(
    name='tests',
    sources=["**/test_*.py"
])

python_distribution(
    name="dist-definition",
    dependencies=[ ":modular_provider_architecture_definition" , ":python-architecture-linter" ],
    provides=setup_py(
        name="modular_provider_architecture_definition",
        version="2.21.0",
        description="An example distribution built with Pants.",
        author="Pantsbuild",
        classifiers=[
            "Programming Language :: Python :: 3.7",
        ],
    ),
    setup_py_commands=["sdist", "bdist_wheel", "--python-tag", "py36.py37"]
)
