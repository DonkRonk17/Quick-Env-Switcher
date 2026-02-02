#!/usr/bin/env python3
"""
Quick Environment Switcher - Setup Script
==========================================
Package configuration for pip installation.

Install:
    pip install -e .  (development mode)
    pip install .     (production mode)

Author: Logan Smith / Metaphy LLC
License: MIT
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="quick-env-switcher",
    version="1.0.0",
    author="Logan Smith",
    author_email="logan@metaphysicsandcomputing.com",
    description="Instantly switch between project environments with a single command",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonkRonk17/quick-env-switcher",
    project_urls={
        "Bug Reports": "https://github.com/DonkRonk17/quick-env-switcher/issues",
        "Source": "https://github.com/DonkRonk17/quick-env-switcher",
    },
    
    # Single module, not a package
    py_modules=["envswitch"],
    
    # Entry points for CLI
    entry_points={
        "console_scripts": [
            "envswitch=envswitch:main",
        ],
    },
    
    # Python version requirement
    python_requires=">=3.8",
    
    # No external dependencies - pure Python stdlib
    install_requires=[],
    
    # Development dependencies
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
    ],
    
    # Keywords for discovery
    keywords="environment, virtualenv, venv, project, switch, development, workflow",
    
    # Include additional files
    include_package_data=True,
)
