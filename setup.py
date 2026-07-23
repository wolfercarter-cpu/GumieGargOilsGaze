from setuptools import setup, find_packages

setup(
    name="oil_garg_gum",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["col", "gaze"],
    include_package_data=True,
    package_data={
        "oil_pkg": ["*.tcss"],  # Keeps your Textual CSS styling intact for editor.py
    },
    install_requires=[
        "textual",
        "rich",
        "ollama",
    ],
    entry_points={
        "console_scripts": [
            "oil=oil_pkg.cli:main",
            "col=col:main",
            "gaze=gaze:main",
        ],
    },
    author="Otakumafia",
    description="The complete GumieGargoil state engine, command runner, and AI copilot suite.",
    python_requires=">=3.8",
)
