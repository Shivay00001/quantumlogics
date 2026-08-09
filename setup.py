from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quantumlogics",
    version="1.0.0",
    author="Quantum Emulation OS Team",
    author_email="example@example.com",
    description="A Unified Quantum-Emulation OS simulating 32 quantum capabilities on classical hardware via Tensor Networks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/quantumlogics",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires='>=3.9',
    install_requires=[
        "fastapi",
        "uvicorn",
        "torch",
        "numpy",
        "pydantic"
    ],
)
