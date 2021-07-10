python_library(
    name="python_architecture_linter",
    sources=["**/*.py", "!tests/*/**", "!tests/**"],
    dependencies=[':astroid'],
)

poetry_requirements()

python_tests(
    name='tests',
    sources=["**/test_*.py"]
)

python_distribution(
    name="dist",
    dependencies=[
        ':python_architecture_linter'
    ],
    provides=setup_py(
        name="python_architecture_linter",
        version="0.1.3",
        description="Core lib for linter.",
        author="Brian Graham",
        classifiers=[
            "Programming Language :: Python :: 3.9",
        ],
    ),
    setup_py_commands=["sdist", "bdist_wheel", "--python-tag", "py36.py37"]
)
