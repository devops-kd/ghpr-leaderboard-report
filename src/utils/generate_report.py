from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import json

def generate_report_from_j2_template(summary):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('files/template.j2')
    rendered_json = template.render(open_pr=summary["opened"],
                                    merged_pr=summary["merged"],
                                    closed_pr=summary["closed"])
    return json.loads(rendered_json)