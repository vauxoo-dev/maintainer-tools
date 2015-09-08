#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script to add autopep8 and CamelizeClass
to Github projects.
'''

import argparse
import subprocess
import os

org = "Vauxoo"
org_prod = "vauxoo"
org_dev = "vauxoo-dev"
branch_list = []
series = ['8.0']


# Creating directories and branches.
def create_repo_branches(repobases,
                         repodevs,
                         author,
                         pull_request=False):
    '''
    Method to create remote base repos and remote developer remotes,
    fix autopep8 and do pull request.
    '''
    cont = 0
    pull_request = pull_request

    for repo in repobases:
        # Split the ssh repobase to the name of the repo.
        # e.g. 'git@github.com:vauxoo-dev/maintainer-tools.git'
        # to 'maintainer-tools'
        repo.strip('/.')
        repo_name = repo[22:-4]
        print repo_name

        # Create directories of the repobases.
        git_repo_path = os.path.join("/home/odoo/projects", repo_name)
        git_repo_path_branch = os.path.join("/home/odoo/projects",
                                            repo_name,
                                            ".git")
        cmd = ['mkdir', '-p', git_repo_path]
        subprocess.call(cmd)

        # Make your dir a github repo.
        cmd = ['git', 'init', git_repo_path]
        subprocess.call(cmd)

        # Add a remote repo to the list of registered repos.
        cmd = ['git', '--git-dir=' + os.path.join(git_repo_path, '.git'),
               'remote', 'add', org_prod, repo]
        subprocess.call(cmd)
        print cmd

        cmd = ['git', '--git-dir=' + os.path.join(git_repo_path, '.git'),
               'remote', 'add', org_dev, repodevs[cont]]
        subprocess.call(cmd)
        print cmd
        cont = cont + 1

        # Bringing all changes from the remote repo
        cmd = ['git', '--git-dir=' + os.path.join(git_repo_path, '.git'),
               'fetch', '--all']
        subprocess.call(cmd)
        print cmd

        cmd = ['git', 'branch', '-a']
        subprocess.call(cmd)

        # Create branch
        # Watch out with this!
        # if you include --git-dir the files
        # will be added to your current folder,
        # not to the specific --git-dir
        # Please use it inside of the folder you want to pull
        cmd = ['git', '--git-dir=' + git_repo_path_branch, 'checkout',
               '-b', '8.0-ref-autopep8-' + repo_name + '-dev-' +
               author.lower(), '--track', 'vauxoo/8.0']
        subprocess.call(cmd)
        print cmd

        # Modify with oca-autopep8
        cmd = ['oca-autopep8', '-ri', git_repo_path]
        subprocess.call(cmd)

        # Checking changes in repo
        cmd = ['git', 'diff']
        subprocess.call(cmd)

        # Make a commit
        cmd = ['git', 'commit', '--author', author, '-am',
               "'[REF] " + repo_name + ": Adding autopep8 in modules'"]
        subprocess.call(cmd)
        print cmd

        # Git push
        cmd = ['git', 'push', org_dev,
               '8.0-ref-autopep8-' + repo_name + '-dev-' + author.lower()]
        subprocess.call(cmd)
        print cmd

        # Creating pull request
        if pull_request:
            cmd = ['hub', 'pull-request', '-o', '-b', org + '/' + repo_name +
                   ':' + series[0], '-h', org_dev + ':' + '8.0-ref-autopep8-'
                   + repo_name + '-dev-' + author.lower()]
            print cmd
            subprocess.call(cmd)


def main():
    '''
    Method main to get args and call other methods.
    '''

    parser = argparse.ArgumentParser()

    parser.add_argument("remotebase",
                        help="The names of the git remote base to use."
                        " Use remote bases names comma separated without \
                         spaces"
                        " e.g. 'git@github.com:Vauxoo/maintainer-tools.git,\
                        git@github.com:Vauxoo/demo-gitflow.git'",
                        type=str)

    parser.add_argument("remotedev",
                        help="The names of the git developer remote to use."
                        " Use dev remote names comma separated without \
                        spaces."
                        " e.g. 'git@github.com:vauxoo-dev/maintainer-tools.\
                        git,git@github.com:vauxoo-dev/demo-gitflow.git'",
                        type=str)

    parser.add_argument("author",
                        help="Name from the autor. Username from Github.",
                        type=str)

    parser.add_argument("--pullrequest",
                        dest="pull_request",
                        action='store_true')

    parser.add_argument("--no-pullrequest",
                        dest="pull_request",
                        action='store_false')

    parser.set_defaults(pull_request=False)
    args = parser.parse_args()

    # Split the string into a list.
    remote_base_list = args.remotebase.split(',')
    print "remote_base_list", remote_base_list
    remote_dev_list = args.remotedev.split(',')
    print "remote_dev_list", remote_dev_list
    create_repo_branches(remote_base_list,
                         remote_dev_list,
                         args.author,
                         args.pull_request)

if __name__ == '__main__':
    main()
