import json

from eryx_deploy import DjangoBasicStack, UbuntuMachine, AmazonRDSMachine
from fabric.state import env

secrets = json.load(open('devops/secrets.json'))

env.local_stack = DjangoBasicStack(host=UbuntuMachine.new_local(project_path=secrets['local_project_path']),
                                   project_name='prode',
                                   db_name='prode_local',
                                   db_user=secrets['local_db_user'],
                                   db_password=secrets['local_db_password'],
                                   remote_url='git@github.com:GermanDeSousa/prode-eryx.git',
                                   requirements_file_path='requirements.txt',
                                   virtual_env_path=secrets['local_virtual_env_path'],
                                   major_python_version=3)

env.stacks['staging'] = DjangoBasicStack(host=UbuntuMachine.new_remote(
                                                    hostname='prode.eryx.co',
                                                    ssh_connection=secrets['ssh'],
                                                    project_path=secrets['production_project_path']),
                                         project_name='prode',
                                         db_name='prode',
                                         db_user='postgres',
                                         db_port='5432',
                                         db_password=secrets['production_db_password'],
                                         remote_url='git@github.com:GermanDeSousa/prode-eryx.git',
                                         requirements_file_path='requirements.txt',
                                         virtual_env_path='%s/bootstrap' % secrets['production_project_path'],
                                         major_python_version=3,
                                         )
env.allow_skipping_cmd = True