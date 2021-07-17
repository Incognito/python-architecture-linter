python_library(
    name="python_architecture_linter_grimp_extension",
    sources=["**/*.py", "!tests/**"]
)
poetry_requirements()

python_distribution(
    name="dist_grimp_ext",
    dependencies=[ 
        ":python_architecture_linter_grimp_extension"
    ],
    provides=setup_py(
        name="python_architecture_linter_grimp_extension",
        version="0.1.1",
        description="Plug grimp into python-architecture-linter",
        author="Brian Graham",
        classifiers=[
            "Programming Language :: Python :: 3.9",
        ],
    ),
    setup_py_commands=["sdist", "bdist_wheel", "--python-tag", "py36.py37"]
)
