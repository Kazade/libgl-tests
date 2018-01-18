# libGL-tests

This is a set of Python scripts and C files which compiles libGL and test apps using the kazade/dreamcast-sdk Docker image and then runs them withe lxdream emulator. This is so that I can more quickly develop libGL without breaking it!

# Usage:

- Run `git submodule update --init`
- Install docker and lxdream
- python runtests.py

libGL is a submodule to my fork of libGL.
