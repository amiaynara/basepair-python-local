'''Project dataype class'''

import json
import sys
# App imports
from basepair.helpers import eprint
from bin.common_parser import add_common_args, add_payload_args, add_json_parser, add_uid_parser

class Project:
  '''Project action methods'''

  @staticmethod
  def create_project(bp_api, args):
    '''Create project'''
    data = {'name': args.name}
    bp_api.create_project(data=data)

  @staticmethod
  def list_project(bp_api, args):
    '''List pipelines'''
    bp_api.print_data(data_type='projects', is_json=args.json)

  @staticmethod
  def update_project(bp_api, args):
    '''Update project'''
    data = {}
    if args.name:
      data = {'name': args.name}

    params = {}

    if args.emails and args.perm:
      params = {
        'params': json.dumps({
          'permission_data': {
            'emails': args.emails,
            'perm': args.perm,
          }
        })
      }
    
    if args.emails and not params:
      sys.exit('ERROR: You have not provided any permission to update.')

    if not data and not params:
      sys.exit('ERROR: You have not provided any data to update.')

    for project_id in args.uid:
      bp_api.update_project(project_id, data=data, params=params)
    return

  @staticmethod
  def project_action_parser(action_parser):
    '''project parser'''

    # create project parser
    create_project_p = action_parser.add_parser(
      'create',
      help='Add a project to your account on Basepair.'
    )
    create_project_p.add_argument(
      '--name', required=True
    )
    create_project_p = add_common_args(create_project_p)

    # list project parser
    list_project_p = action_parser.add_parser(
      'list',
      help='List all projects on Basepair.'
    )
    list_project_p = add_common_args(list_project_p)
    list_project_p = add_json_parser(list_project_p)

    # update project parser
    update_project_parser = action_parser.add_parser(
      'update',
      help='Update information associated with a project.'
    )
    update_project_parser = add_common_args(update_project_parser)
    update_project_parser.add_argument('--emails', default=[], nargs='+')
    update_project_parser.add_argument('--name')
    update_project_parser.add_argument(
      '--perm', choices=['admin', 'edit', 'view'], default='view')
    update_project_parser = add_uid_parser(update_project_parser, 'project')

    return action_parser
