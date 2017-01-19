#!/Users/rmartini/.virtualenvs/pynet/bin/python
'''
Script to create an ansible playbook structure
'''

import argparse
import os
import sys
import yaml

DEBUG = True

class Playbook:
    '''
    Class create an Ansible playbook skeleton
    source: http://docs.ansible.com/ansible/playbooks_best_practices.html
    tree:
        site.yml                  # master playbook
        roles/
            common/               # this hierarchy represents a "role"
                tasks/            #
                    main.yml      #  <-- tasks file can include smaller files if warranted
                templates/        #  <-- files for use with the template resource
                    template.j2   #  <------- templates end in .j2
                vars/             #
                    main.yml      #  <-- variables associated with this role
    '''
    role_skeleton = [
        {'name': 'tasks',
         'files': ['main.yml']
         },
        {'name': 'templates',
         'files': []
         },
        {'name': 'vars',
         'files': ['main.yml']
         }
    ]

    def __init__(self, *args, **kwargs):
        if args:
            self.name = args[0]
            self.roles = args[1]
            self.path = args[2]
        elif kwargs:
            self.name = kwargs['name']
            self.roles = kwargs['roles']
            self.path = kwargs['path']
        else:
            self.name = 'playbook'
            self.roles = ['role1']
            self.path = '.'
        self.pb_path = '{}/{}'.format(self.path, self.name)

    def write_site_yml(self):
        '''
        Creates the site.yml file for the playbook
        :param file:
        :param roles:
        :return:
        '''
        '''Example:
        ---
        - name: Playbook
          hosts: local
          roles:
          - role1
          - role2
        '''
        file = '{}/site.yml'.format(self.pb_path)
        yaml_data = [{
            'hosts': 'local',
            'name': self.name,
            'roles': self.roles
        }]
        with open(file, 'w') as f:
            f.write('---\n')
            f.write('#Template for Playbook "{}"\n'.format(self.name))
            f.write(yaml.dump(yaml_data,default_flow_style=False))
        return

    def write_role(self):
        '''
        Build the skeleton for a new role
        :return:
        '''
        pass

    def write(self):
        '''
        Builds all the folders defined in the skeleton
        :return:
        '''
        if DEBUG:
            try:
                os.makedirs(self.pb_path)
            except:
                pass
        else:
            # check if the main folder exsists before creating it
            if not os.path.exists(self.pb_path):
                os.makedirs(self.pb_path)
            else:
                sys.exit('The Directory already exist, not going to mess with it')
        roles_dir = '{}/roles'.format(self.pb_path)
        self.write_site_yml()
        os.makedirs(roles_dir)
        for role in self.roles:
            role_dir = '{}/{}'.format(roles_dir,role)
            os.makedirs(role_dir)
            for folder in self.role_skeleton:
                # create the folder
                folder_path = '{}/{}'.format(role_dir,folder['name'])
                os.makedirs(folder_path)
                for filename in folder['files']:
                    file = '{}/{}'.format(folder_path,filename)
                    with open(file, 'w') as f:
                        f.write('---\n')
                        f.write('#role: {}/{}\n'.format(role,folder['name']))
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates the template for an ansible playbook')
    parser.add_argument('name',
                        default='playbook_name',
                        nargs='?',
                        # action='append',
                        help='playbook name'
                        )
    parser.add_argument('roles',
                        nargs='*',
                        default=['role'],
                        help='role'
                        )
    parser.add_argument('--path', '-p',
                        default='.',
                        nargs='?')
    # parser.set_defaults(pb_name='playbook', roles=['role'], path='.')
    # the vars will load the Namespace returned from the parse_args into a dict
    args = parser.parse_args()
    kwargs = vars(args)
    print('Generating the <{}> playbook in {}'.format(args.name, args.path))
    Playbook(**kwargs).write()
    print('Done!')












