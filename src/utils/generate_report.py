'''
This module generates the report from the je template using jinija2 library.
'''

import json
from jinja2 import Environment, FileSystemLoader


def generate_report_from_j2_template(summary):
    '''
    The function that loads the jinja template and generates a report with pr data.
    '''
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('files/template.j2')
    rendered_json = template.render(open_pr=summary["opened"],
                                    merged_pr=summary["merged"],
                                    closed_pr=summary["closed"])
    return json.loads(rendered_json)
