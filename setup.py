
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from setuptools import Extension, setup, find_packages
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py

try:
    subprocess.check_output(['ninja', '--version'])
except:
    subprocess.check_output([sys.executable, '-m', 'pip', 'install', 'ninja'])
try:
    import cmake
except ModuleNotFoundError:
    subprocess.check_output([sys.executable, '-m', 'pip', 'install', 'cmake'])


# Convert distutils Windows platform specifiers to CMake -A arguments
PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}

CURDIR = os.path.dirname(os.path.abspath(__file__))
BUILD_RASPBERRY = os.environ.get('BUILD_RASPBERRY', '')
RASPBIAN_ROOTFS = os.path.abspath(os.path.expanduser(os.path.expandvars(os.environ.get('RASPBIAN_ROOTFS', '~/rpi/rootfs'))))
RASPBERRY_VERSION = os.environ.get('RASPBERRY_VERSION', '3')
RASPBERRY_PYTHON_VERSION = os.environ.get('RASPBERRY_PYTHON_VERSION', '3.9')

if os.environ.get('BUILD_RASPBERRY', '') == '1':
    sys.argv.extend(['--plat-name', 'linux_armv7l'])
    PYTHON_MODULE_EXTENSION = f'.cp{RASPBERRY_PYTHON_VERSION.replace(".", "")}-cp{RASPBERRY_PYTHON_VERSION.replace(".", "")}-linux_armv7l.so'


# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name: str, sourcedir: str = "") -> None:
        super().__init__(name, sources=[])
        self.sourcedir = os.fspath(Path(sourcedir).resolve())


class CMakeBuild(build_ext):
    def build_extension(self, ext: CMakeExtension) -> None:
        import cmake

        ext.name = '_qrcode_detector'
        ext._full_name = '_qrcode_detector'
        ext._file_name = '_' + ext._file_name

        # Must be in this form due to bug in .resolve() only fixed in Python 3.10+
        ext_fullpath = Path.cwd() / self.get_ext_fullpath(ext.name)  # type: ignore[no-untyped-call]
        extdir = ext_fullpath.parent.resolve()

        # Using this requires trailing slash for auto-detection & inclusion of
        # auxiliary "native" libs

        debug = int(os.environ.get("DEBUG", 0)) if self.debug is None else self.debug
        cfg = "Debug" if debug else "Release"

        # CMake lets you override the generator - we need to check this.
        # Can be set with Conda-Build, for example.
        cmake_generator = os.environ.get("CMAKE_GENERATOR", "")

        os.environ['RASPBIAN_ROOTFS'] = RASPBIAN_ROOTFS
        os.environ['RASPBERRY_VERSION'] = RASPBERRY_VERSION

        PYTHON_EXECUTABLE = os.environ.get(
            'PYTHON_EXECUTABLE', 
            sys.executable if not BUILD_RASPBERRY else f'{RASPBIAN_ROOTFS}/usr/bin/python{RASPBERRY_PYTHON_VERSION}')

        # Set Python_EXECUTABLE instead if you use PYBIND11_FINDPYTHON
        # EXAMPLE_VERSION_INFO shows you how to pass a value into the C++ code
        # from Python.
        cmake_args = [
            f"-DPYTHON_EXECUTABLE={PYTHON_EXECUTABLE}",
            f"-DCMAKE_BUILD_TYPE={cfg}",  # not used on MSVC, but no harm
        ]

        if BUILD_RASPBERRY == '1':
            ext._file_name = '_qrcode_detector'+ PYTHON_MODULE_EXTENSION
            cmake_args.append(f'-DCMAKE_TOOLCHAIN_FILE={CURDIR}/cpp/toolchain-rpi.cmake')
            cmake_args.append(f'-DPYTHONLIBS_FOUND=1')
            cmake_args.append(f'-DPYTHON_MODULE_EXTENSION={PYTHON_MODULE_EXTENSION}')
            cmake_args.append(f'-DPYTHON_PREFIX={RASPBIAN_ROOTFS}/usr')
            cmake_args.append(f'-DPYTHON_LIBRARIES={RASPBIAN_ROOTFS}/usr/lib/python{RASPBERRY_PYTHON_VERSION}')
            cmake_args.append(f'-DPYTHON_INCLUDE_DIRS={RASPBIAN_ROOTFS}/usr/include/python{RASPBERRY_PYTHON_VERSION}')
            cmake_args.append(f'-DPYTHON_MODULE_PREFIX=')

        build_args = []
        # Adding CMake arguments set as environment variable
        # (needed e.g. to build for ARM OSx on conda-forge)
        if "CMAKE_ARGS" in os.environ:
            cmake_args += [item for item in os.environ["CMAKE_ARGS"].split(" ") if item]

        if self.compiler.compiler_type != "msvc":
            # Using Ninja-build since it a) is available as a wheel and b)
            # multithreads automatically. MSVC would require all variables be
            # exported for Ninja to pick it up, which is a little tricky to do.
            # Users can override the generator with CMAKE_GENERATOR in CMake
            # 3.15+.
            if not cmake_generator or cmake_generator == "Ninja":
                try:
                    import ninja  # noqa: F401

                    ninja_executable_path = Path(ninja.BIN_DIR) / "ninja"
                    cmake_args += [
                        "-GNinja",
                        f"-DCMAKE_MAKE_PROGRAM:FILEPATH={ninja_executable_path}",
                    ]
                except ImportError:
                    pass

        else:

            # Single config generators are handled "normally"
            single_config = any(x in cmake_generator for x in {"NMake", "Ninja"})

            # CMake allows an arch-in-generator style for backward compatibility
            contains_arch = any(x in cmake_generator for x in {"ARM", "Win64"})

            # Specify the arch if using MSVC generator, but only if it doesn't
            # contain a backward-compatibility arch spec already in the
            # generator name.
            if not single_config and not contains_arch:
                cmake_args += ["-A", PLAT_TO_CMAKE[self.plat_name]]
                cmake_args += ['-T', 'host=x86']
                cmake_args += ['-G', 'Visual Studio 16 2019']

            # Multi-config generators have a different way to specify configs
            if not single_config:
                build_args += ["--config", cfg]

        if sys.platform.startswith("darwin"):
            # Cross-compile support for macOS - respect ARCHFLAGS if set
            archs = re.findall(r"-arch (\S+)", os.environ.get("ARCHFLAGS", ""))
            if archs:
                cmake_args += ["-DCMAKE_OSX_ARCHITECTURES={}".format(";".join(archs))]

        # Set CMAKE_BUILD_PARALLEL_LEVEL to control the parallel build level
        # across all generators.
        if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
            # self.parallel is a Python 3 only way to set parallel jobs by hand
            # using -j in the build_ext call, not supported by pip or PyPA-build.
            if hasattr(self, "parallel") and self.parallel:
                # CMake 3.12+ only.
                build_args += [f"-j{self.parallel}"]


        src_dir = os.path.abspath(f'{ext.sourcedir}/cpp').replace('\\', '/')
        build_temp = os.path.abspath(f'{self.build_temp}/{ext.name}').replace('\\', '/')
        os.makedirs(build_temp, exist_ok=True)


        try:
            os.remove(f'{build_temp}/CMakeCache.txt')
        except:
            pass
        cmd = ['cmake', f'-S{src_dir}', f'-B{build_temp}'] + cmake_args
        self.announce(' '.join(cmd))
        subprocess.check_output(cmd, env=os.environ)

        cmd =  ['cmake', "--build", build_temp, '--target', 'QRCodeDetector_wrapper'] + build_args
        self.announce(' '.join(cmd))
        subprocess.check_output(cmd , cwd=build_temp, env=os.environ)
        shutil.copy(f'{ext.sourcedir}/qrcode_detector/{ext._file_name}', f'{self.build_lib}/qrcode_detector/{ext._file_name}')

    def copy_extensions_to_source(self):
        pass

setup(
    name='qrcode_detector',
    version='0.1.0',
    description='Robust implementation for detecting QR codes',
    author='Dan Riedler',
    url='https://github.com/driedler/qrcode_detector',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7,<3.11',
    packages=find_packages(include=['qrcode_detector', 'qrcode_detector.*']),
    install_requires=[
        'numpy>=1.14.5'
    ],
    ext_modules=[CMakeExtension("qrcode_detector")],
    cmdclass={
        'build_ext': CMakeBuild,
    },
)