#!/usr/bin/env python

import argparse
import datetime
import os

import jinja2
import pytz
from pytz import timezone


def parse_args():
    parser = argparse.ArgumentParser(
        description='Create a static website for LDM-148.'
    )
    parser.add_argument(
        'template_path',
        help='Path of the index.html Jinja2 template.'
    )
    parser.add_argument(
        'deploy_dirname',
        help='Directory where the built index.html should be added '
             'for deployment.'
    )
    return parser.parse_args()


def main():
    args = parse_args()

    loader = jinja2.FileSystemLoader(os.path.dirname(args.template_path))
    template_env = jinja2.Environment(
        loader=loader,
        autoescape=jinja2.select_autoescape(['html', 'xml']))
    template = template_env.get_template(os.path.basename(args.template_path))

    utc = pytz.utc
    pacific_tz = timezone('US/Pacific')
    pacific_dt = pacific_tz.normalize(datetime.datetime.utcnow().
                                      replace(tzinfo=utc))

    html = template.render(
        branch_name=os.getenv('TRAVIS_BRANCH'),
        pacific_timestring=pacific_dt.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
        page_title='LDM-148: Data Management System Design',
        page_description='Draft of LDM-148, the LSST Data Management '
                         'System Design document.'
    )
    index_html_path = os.path.join(args.deploy_dirname, 'index.html')
    with open(index_html_path, mode='w') as f:
        f.write(html)


if __name__ == '__main__':
    main()
