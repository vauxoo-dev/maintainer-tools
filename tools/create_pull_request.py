# -*- coding: utf-8 -*-

'''
Script to create pull request from a repo/branch to other repo
'''

import argparse
import re
import requests
import simplejson
import sys

import github3

from github_login import login, read_config, CREDENTIALS_FILE

def github(repo_base, url, payload=None, delete=False):
    """Return a http request to be sent to github"""
    config = read_config(CREDENTIALS_FILE)
    token = config.get('GitHub', 'token')
    if not token:
        raise Exception('Does not have a token to authenticate')
    match_object = re.search('([^/]+)/([^/]+)/([^/.]+(.git)?)', repo_base)
    if match_object:
        url = url.replace(':owner', match_object.group(2))
        url = url.replace(':repo', match_object.group(3))
        url = 'https://api.%s%s' % (match_object.group(1),url)
        print "url",url
        session = requests.Session()
        session.auth = (token,'x-oauth-basic')
        session.headers.update({'Accept': 'application/vnd.github.she-hulk-preview+json'})
        if payload:
            response = session.post(url, data=simplejson.dumps(payload))
        elif delete:
            response = session.delete(url)
        else:
            response = session.get(url)
        print url
        return response.json()

#def create_pull_request(repo_from, branch_from, repo_to, branch_to):
def create_pull_request(repo_base, branch_base, branch_dest, title, comment=None):
    '''
    Method to make pull request from a repo/branch to other repo
    @repo_base Repo where show pr
    @branch_dest Branch name destination use username:branchname
    '''
    #gh_login = login()
    #import pdb;pdb.set_trace()
    #github3.pulls.PullRequest()
    #repo_base = 'git@github.com:moylop260/odoo-dev.git'
    #repo_base = 'https://github.com/moylop260/odoo-dev'
    #repo_base = 'https://github.com/oca/maintainer-quality-tools'
    pr_data = {
            "title": title,
            "head": branch_dest,
            "base": branch_base,
            "body": comment,
        }
    return github(repo_base=repo_base, url='/repos/:owner/:repo/pulls', payload=pr_data)


def main():
    '''
    Method main to get args and call create_pull_request method
    '''
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_to",
                        help="Destination of organization to fork it all"
                        " repositories",
                        required=True)
    parser.add_argument("--org_from",
                        help="Organization origin to get all repositories."
                        " Default: oca",
                        default='oca')
    args = parser.parse_args()

    #fork(args.org_from, args.org_to)
    """
    #create_pull_request(args.org_from, args.org_to, args.branch)
    #repo_base = 'https://github.com/oca-travis/connector-ecommerce'
    #branch_base = '7.0-autofix-script-01-dev-moylop260'
    repo_base = 'https://github.com/oca/connector-ecommerce'
    branch_base = '7.0'
    
    branch_dest = 'oca-travis:7.0-autofix-script-01-dev-moylop260'
    title = '[7.0] [REF] auto-fix conventions'
    comment = None
    print create_pull_request(repo_base, branch_base, branch_dest, title, comment)


if __name__ == '__main__':
    main()
