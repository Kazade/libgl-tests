#!/bin/env python

import subprocess
from os.path import abspath


DOCKER_IMAGE = "kazade/dreamcast-sdk"
VOLUME_MOUNT = "/libgl-tests"


def run_docker_command(command):
    return subprocess.call(
        'sudo docker run -v {this_dir}:{mount}:Z --workdir={mount} {image} /bin/sh -c "{command}"'.format(
            image=DOCKER_IMAGE, command=command, mount=VOLUME_MOUNT, this_dir=abspath(".")
        ), shell=True
    )


def build_libgl():
    return run_docker_command(
        "ls -l; cd libgl; make"
    )

if __name__ == '__main__':
    build_libgl()
