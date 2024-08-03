import os
import shutil

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import download, unzip, patch

class JwtppConan(ConanFile):
  name = "jwtpp"
  settings = "os", "compiler", "build_type", "arch"
  exports_sources = "*.patch"

  def requirements(self):
    for dependency in self.conan_data[str(self.version)]["dependencies"]:
      self.requires(dependency)

  def source(self):
    # Download source from github
    zip_name = f"{self.name}-v{self.version}.zip"
    download(self, self.conan_data[self.version]['url'], zip_name)
    # Unzip and remove zip
    unzip(self, zip_name)
    shutil.move(f"{self.name}-{self.version}", self.name)
    os.unlink(zip_name)
    # patch CMakeLists
    patch_file = os.path.join(self.export_sources_folder, "CMakeLists.txt.patch")
    patch(self, patch_file=patch_file)

  def generate(self):
    deps = CMakeDeps(self)
    deps.generate()
    tc = CMakeToolchain(self)
    tc.generate()

  def build(self):
    cmake = CMake(self)
    cmake.configure(build_script_folder=self.name)
    cmake.build()

  def package(self):
    cmake = CMake(self)
    cmake.install()
