python_library(
    name="modular_provider_architecture_definition",
    sources=["**/*.py", "!tests/**"],
    dependencies=[':astroid'],
)
poetry_requirements()

python_tests(
    name='tests',
    sources=["**/test_*.py"
])

python_distribution(
    name="dist_definition",
    dependencies=[ 
        ":modular_provider_architecture_definition" 
    ],
    provides=setup_py(
        name="modular_provider_architecture_definition",
        version="0.1.1",
        description="An example distribution built with Pants.",
        author="Pantsbuild",
        classifiers=[
            "Programming Language :: Python :: 3.7",
        ],
    ),
    setup_py_commands=["sdist", "bdist_wheel", "--python-tag", "py36.py37"]
)
