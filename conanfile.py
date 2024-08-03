import os
import shutil

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps
from conan.tools.files import download, unzip, patch

class JwtppConan(ConanFile):
  name = "jwtpp"
  version = "2.0.5"
  settings = "os", "compiler", "build_type", "arch"
  exports_sources = "*.patch"

  def requirements(self):
    self.requires("jsoncpp/1.9.5")
    self.requires("openssl/3.2.2")

  def generate(self):
    deps = CMakeDeps(self)
    deps.generate()
    tc = CMakeToolchain(self)
    tc.generate()

  def source(self):
    # Download source from github
    remote_zip_name = f"v{self.version}.zip"
    zip_name = f"{self.name}-v{self.version}.zip"
    download(self, f"https://github.com/troian/jwtpp/archive/refs/tags/{remote_zip_name}", zip_name)
    # Unzip and remove zip
    unzip(self, zip_name)
    shutil.move(f"jwtpp-{self.version}", "jwtpp")
    os.unlink(zip_name)
    # patch CMakeLists
    patch_file = os.path.join(self.export_sources_folder, "CMakeLists.txt.patch")
    patch(self, patch_file=patch_file)
