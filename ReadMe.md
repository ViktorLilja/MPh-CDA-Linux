# MPh-CDA-Linux
This is a fork of MPh version 1.2.3 adapted to work on the Linux computers administrated by Chalmers University of Technology (CDA-Linux). The file discovery.py has been modified with a hard-coded path the the CDA Linux custom installation location of Comsol 6.2.

Confirmed working 2023-01-17.

Written originally by Albin Jonasson Svärdsby, tweaked by Viktor Lilja.

## Example usage with pip
Clone this repository to for example *
`/chalmers/users/<cid>/pythonmodules/MPh-CDA-Linux/`. Then pip install to your python environment using 

    pip install -e /chalmers/users/<cid>/pythonmodules/MPh-CDA-Linux

MPh can then be used as normal:

    import mph

    # mph.option('classkit',True) # Try if you have problems with licenses
    client = mph.start()


## Original ReadMe below:

# MPh
*Pythonic scripting interface for Comsol Multiphysics*

[Comsol] is a commercial software application that is widely used in
science and industry for research and development. It excels at modeling
almost any (multi-)physics problem by solving the governing set of
partial differential equations via the finite-element method. It comes
with a modern graphical user interface to set up simulation models and
can be scripted from Matlab or its native Java API.

MPh brings the dearly missing power of Python to the world of Comsol.
It leverages the Java bridge provided by [JPype] to access the Comsol
API and wraps it in a layer of pythonic ease-of-use. The Python wrapper
covers common scripting tasks, such as loading a model from a file,
modifying parameters, importing data, to then run the simulation,
evaluate the results, and export them.

Comsol models are marked by their `.mph` file extension, which stands
for multi-physics. Hence the name of this library. It is open-source
and in no way affiliated with Comsol Inc., the company that develops
and sells the simulation software.

Find the full [documentation on Read-the-Docs][docs].

[Comsol]: https://www.comsol.com
[JPype]:  https://github.com/jpype-project/jpype
[docs]:   https://mph.readthedocs.io

[![release page](
    https://img.shields.io/pypi/v/mph.svg?label=release)](
    https://pypi.python.org/pypi/mph)
[![download statistics](
    https://img.shields.io/pypi/dm/MPh)](
    https://pypistats.org/packages/mph)
[![scientific citation](
    https://zenodo.org/badge/264718959.svg)](
    https://zenodo.org/badge/latestdoi/264718959)
[![coverage report](
    https://img.shields.io/codecov/c/github/MPh-py/MPh?token=02ZZ8ZJH3M)](
    https://codecov.io/gh/MPh-py/MPh)
[![latest documentation](
    https://readthedocs.org/projects/mph/badge/?version=latest)](
    https://mph.readthedocs.io/en/latest)