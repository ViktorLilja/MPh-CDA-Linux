"""
Discovers Comsol installations.

This is an internal helper module that is not part of the public API.
It retrieves information about installed Comsol versions, i.e.
available simulation back-ends, and locates the installation folders.

In MPh-CDA-Linux, this file has been adapted to only work on Chalmers CDA Linux
computers, and only Chalmers CDA Linux computers. The Comsol installation
location is hard-coded in the search_chalmers_linux function.
"""
__license__ = 'MIT'


########################################
# Dependencies                         #
########################################
import platform                        # platform information
import re                              # regular expressions
from subprocess import run, PIPE       # external processes
from functools import lru_cache        # function cache
from pathlib import Path               # file paths
from sys import version_info           # Python version
from logging import getLogger          # event logging


########################################
# Globals                              #
########################################
logger = getLogger(__package__)        # event logger
system = platform.system()             # operating system


########################################
# Version information                  #
########################################

def parse(version):
    """
    Parses version information as returned by Comsol executable.

    Returns `(name, major, minor, patch, build)` where `name` is a
    string and the rest are numbers. The name is a short-hand based
    on the major, minor, and patch version numbers, e.g. `'5.3a'`.

    Raises `ValueError` if the input string deviates from the expected
    format, i.e., the format in which the Comsol executable returns
    version information.
    """

    # Separate version number from preceding program name.
    match = re.match(r'(?i)Comsol.*?(\d+(?:\.\d+)*)', version)
    if not match:
        raise ValueError(f'Version info "{version}" has invalid format.')
    number = match.group(1)

    # Break the version number down into parts.
    parts = number.split('.')
    if len(parts) > 4:
        raise ValueError(f'Version number "{number}" has too many parts.')
    try:
        parts = [int(part) for part in parts]
    except ValueError:
        error = f'Not all parts of version "{number}" are numbers.'
        raise ValueError(error) from None
    parts = parts + [0]*(4-len(parts))
    (major, minor, patch, build) = parts

    # Assign a short-hand name to this version.
    name = f'{major}.{minor}'
    if patch > 0:
        name += chr(ord('a') + patch - 1)

    # Return version details.
    return (name, major, minor, patch, build)


########################################
# Discovery mechanism                  #
########################################

def search_chalmers_linux():
    """Searches for Comsol installations on a Linux system."""

    # Collect all information in a list.
    print("Searching for COMSOL within Chalmers file system")
    
    # Manually specify paths to installation within Chalmers system
    base   = "/chalmers/sw/sup64/comsol-6.2"
    root   = Path(base + "/installed")
    comsol = Path(base + "/wbin/comsol")
    java   = Path(base + "/installed/java/glnxa64/jre/bin")
    jvm    = Path(base + "/installed/java/glnxa64/jre/lib/server/libjvm.so")
    api    = Path(base + "/installed/plugins")
    lib    = Path(base + "/installed/glnxa64")
    gra    = Path(base + "/installed/ext/graphicsmagick/glnxa64")

    # Get version information from Comsol server.
    process = run([comsol, 'server', '--version'], stdout=PIPE)
    if process.returncode != 0:
        logger.warning('Querying version information failed.')
    version = process.stdout.decode('ascii', errors='ignore').strip()
    print(f'Running "{version}"')

    # Attempt to parse version string
    try:
        (name, major, minor, patch, build) = parse(version)
    except ValueError as error:
        logger.warning("Unable to parse version string, setting arbitrary values")
        (name, major, minor, patch, build) = ("6.2",6,2,None,666)
    
    # Collect all information in a dictionary and add it to a list.
    backends = []
    backends.append({
        'name':   name,
        'major':  major,
        'minor':  minor,
        'patch':  patch,
        'build':  build,
        'root':   root,
        'jvm':    jvm,
        'server': [comsol, 'mphserver'],
    })
    
    # Return list with information about all installed Comsol back-ends.
    return backends


@lru_cache(maxsize=1)
def search_system():
    """Searches the system for Comsol installations."""
    if system == 'Linux':
        return search_chalmers_linux()
    else:
        print("This fork of MPh only supports Chalmers Linux systems")
        error = f'Unsupported operating system "{system}".'
        logger.error(error)
        raise NotImplementedError(error)


########################################
# Back-end selection                   #
########################################

def backend(version=None):
    """
    Returns information about the Comsol back-end.

    A specific Comsol `version` can be selected by name if several
    are installed, for example `version='5.3a'`. Otherwise the latest
    version is used.
    """
    backends = search_system()
    if not backends:
        error = 'Could not locate any Comsol installation.'
        logger.error(error)
        raise RuntimeError(error)
    if version is None:
        numbers = [(backend['major'], backend['minor'], backend['patch'],
                   backend['build']) for backend in backends]
        return backends[numbers.index(max(numbers))]
    else:
        names = [backend['name'] for backend in backends]
        if version not in names:
            error = f'Could not locate Comsol {version} installation.'
            logger.error(error)
            raise LookupError(error)
        return backends[names.index(version)]
