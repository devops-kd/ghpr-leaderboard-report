'''
This module generates the report from the j2 template using jinja2 library.
'''

import json
from jinja2 import Environment, FileSystemLoader


def generate_report_from_j2_template(summary):
    '''
    Ths function loads the jinja template and generates a report with pr data.

    Parameter:
    summary(dict): Processed summary of PR data that has opened, closed and merged
                   pull requests since the given no. of days ago, usually the previous week.
    '''
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('files/template.j2')
    rendered_json = template.render(open_pr=summary["opened"],
                                    merged_pr=summary["merged"],
                                    closed_pr=summary["closed"])
    return json.loads(rendered_json)
