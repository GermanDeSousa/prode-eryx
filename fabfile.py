from eryx_deploy import *
from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import run

# noinspection PyUnresolvedReferences
from devops import stacks

env.allow_skipping_cmd = True