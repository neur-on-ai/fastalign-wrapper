import subprocess
from pathlib import Path

from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext


class BuildFastAlign(build_ext):
  def run(self):
    build_dir = Path("external/fast_align/build")
    build_dir.mkdir(parents=True, exist_ok=True)

    # Run CMake configuration
    subprocess.check_call(["cmake", ".."], cwd=build_dir)
    # Build fast_align binary
    subprocess.check_call(["make"], cwd=build_dir)

    # Continue with standard build_ext
    super().run()


setup(
    name="fastalign-wrapper",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    cmdclass={"build_ext": BuildFastAlign},
    install_requires=[],
    zip_safe=False,
)
