#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script to add autopep8 and CamelizeClass
to Github projects.
'''

import argparse
import github3
import subprocess
import sys

import os


org_prod = "vauxoo"
org_dev = "vauxoo-dev"
branch_list = []
series = ['8.0']

# Creating directories and branches.

def create_repo_branches(repobases, repodevs, author):
    '''
    Method to create remote base repos
    and remote developer repos.
    '''
    cont = 0
    for repo in repobases:
        # Split the ssh repobase to the name of the repo.
        # e.g. 'git@github.com:vauxoo-dev/maintainer-tools.git' to 'maintainer-tools'
        repo.strip('/.')
        repo_name = repo[22:-4]
        print repo_name

        # Create directories of the repobases.
        git_repo_path = os.path.join("/home/odoo/projects", repo_name)
        cmd = ['mkdir', '-p', git_repo_path]
        subprocess.call(cmd)
#        os.mkdir(repo)

        # Make your dir a github repo.
        cmd = ['git', 'init', git_repo_path]
        subprocess.call(cmd)

        # Add a remote repo to the list of registered repos.
        cmd = ['git', '--git-dir=' + os.path.join(git_repo_path, '.git'), 'remote', 'add', org_prod, repo]
        subprocess.call(cmd)
        print cmd

        cmd = ['git', '--git-dir=' + os.path.join(git_repo_path, '.git'), 'remote', 'add', org_dev, repodevs[cont]]
        subprocess.call(cmd)
        print cmd
        cont = cont + 1

        # Bringing all changes from the remote repo
        cmd = ['git', '--git-dir=' + os.path.join(git_repo_path, '.git'), 'fetch', '--all']
        subprocess.call(cmd)
        print cmd

        cmd = ['git', 'branch', '-a']
        subprocess.call(cmd)

        # Create branch
        cmd = ['git', 'checkout', '-b', '8.0-ref-autopep8-' + repo_name + '-' + author, '--track', 'vauxoo/8.0']
        subprocess.call(cmd)
        print cmd


def main():
    '''
    Method main to get args and call other methods.
    '''

 
    parser = argparse.ArgumentParser()

    parser.add_argument("remotebase",
                        help="The names of the git remote base to use."
                        " Use remote bases names comma separated without spaces"
                        " e.g. 'git@github.com:Vauxoo/maintainer-tools.git,git@github.com:Vauxoo/demo-gitflow.git'",
                        type=str)

    parser.add_argument("remotedev",
                        help="The names of the git developer remote to use."
                        " Use dev remote names comma separated without spaces \n"
                        " e.g. 'git@github.com:vauxoo-dev/maintainer-tools.git,git@github.com:vauxoo-dev/demo-gitflow.git'",
                        type=str)

    parser.add_argument("author",
                        help="Name from the autor. Username from Github.",
                        type=str)

    args = parser.parse_args()

    # Split the string into a list.    
    remote_base_list = args.remotebase.split(',')
    print "remote_base_list", remote_base_list
    remote_dev_list = args.remotedev.split(',')
    print "remote_dev_list", remote_dev_list
    res = create_repo_branches(remote_base_list, remote_dev_list, args.author)

if __name__ == '__main__':
    main()
