"""Installation script for the nonapod_lab Python package."""

from pathlib import Path
import toml

from setuptools import find_packages, setup

EXTENSION_PATH = Path(__file__).resolve().parent
EXTENSION_TOML_DATA = toml.load(EXTENSION_PATH / "config" / "extension.toml")

setup(
    name="nonapod_lab",
    packages=find_packages(),
    author=EXTENSION_TOML_DATA["package"]["author"],
    maintainer=EXTENSION_TOML_DATA["package"]["maintainer"],
    url=EXTENSION_TOML_DATA["package"]["repository"],
    version=EXTENSION_TOML_DATA["package"]["version"],
    description=EXTENSION_TOML_DATA["package"]["description"],
    keywords=EXTENSION_TOML_DATA["package"]["keywords"],
    license="Apache 2.0",
    include_package_data=True,
    package_data={"nonapod_lab": ["assets/robots/nonapod/*.urdf"]},
    python_requires=">=3.11",
    zip_safe=False,
)
