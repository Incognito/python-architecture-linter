python_library(
    name="grimp_package_metrics",
    sources=["**/*.py", "!tests/**"]
)
poetry_requirements()

#python_tests(
#    name='tests',
#    sources=["**/test_*.py"
#])

python_distribution(
    name="dist_cli",
    dependencies=[ 
        ":grimp_package_metrics",
        ":grimp"
    ],
    provides=setup_py(
        name="grimp_package_metrics",
        version="0.1.0",
        description="An example distribution built with Pants.",
        author="Pantsbuild",
        classifiers=[
            "Programming Language :: Python :: 3.7",
        ],
    ),
    setup_py_commands=["sdist", "bdist_wheel", "--python-tag", "py36.py37"]
)
