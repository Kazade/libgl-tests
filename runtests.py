#!/bin/env python

import subprocess
from os import listdir
from os.path import abspath, join


DOCKER_IMAGE = "kazade/dreamcast-sdk"
VOLUME_MOUNT = "/libgl-tests"


def run_docker_command(command):
    return subprocess.call(
        'sudo docker run -v {this_dir}:{mount}:Z --workdir={mount} {image} /bin/sh -c "{command}"'.format(
            image=DOCKER_IMAGE, command=command, mount=VOLUME_MOUNT, this_dir=abspath(".")
        ), shell=True
    )


def build_libgl():
    return run_docker_command("source /etc/bash.bashrc; cd libgl; make")

def build_tests():
    def generate_makefile(tests):
        lines = []
        targets = []
        for test in tests:
            name = test.rsplit(".",1)[0]
            targets.append(name)

            lines.append("{name}: {name}.o".format(name=name))
            lines.append("\t$(KOS_CC) $(KOS_CFLAGS) $(KOS_LDFLAGS) -o %s $(KOS_START) %s.o $(KOS_LIBS)" % (name, name))

        lines.append("include $(KOS_BASE)/addons/Makefile.prefab")
        lines.append("defaultall: %s" % " ".join(targets))

        with open("tests/Makefile", "w") as fout:
            fout.write("\n".join(lines))

        return targets

    test_sources = [x for x in listdir("tests") if x.endswith(".c")]
    targets = generate_makefile(test_sources)

    ret = run_docker_command('source /etc/bash.bashrc; cd tests; make')
    if ret:
        return ret

    for target in targets:
        command = "lxdream -H -b -e tests/%s" % target
        subprocess.call(command, shell=True)


if __name__ == '__main__':
    build_libgl()
    build_tests()
