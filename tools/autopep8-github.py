#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script to add autopep8, CamelizeClass, create README.rst, 
remove vim comment, remove magic comment interpreter, change coding
comment and automate git commands like:
create branches, commit, push and
do pull request to Github projects.

Requirements

    Oca-autopep8
        - $ git clone git@github.com:OCA/maintainers-tools.git
        - $ cd maintainers-tools
        - $ python setup.py install

    See more info: https://github.com/Vauxoo/maintainer-tools

    Brew previously installed (homebrew or linuxbrew):
        - Linuxbrew
            - Install dependencies:
                - $ sudo apt-get install build-essential curl git m4 ruby
                    texinfo libbz2-dev libcurl4-openssl-dev libexpat-dev
                    libncurses-dev zlib1g-dev
            - Install:
                - $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/linuxbrew/go/install)" '''  # noqa
'''
        - Add to your .bashrc or .zshrc:
            export PATH="$HOME/.linuxbrew/bin:$PATH"
            export MANPATH="$HOME/.linuxbrew/share/man:$MANPATH"
            export INFOPATH="$HOME/.linuxbrew/share/info:$INFOPATH"

            Note: Check you are installing in one of your specific PATH.
                  Use $ env to check your PATHs.

        - If you have troubles installing by curl and ruby use:
            $ git clone https://github.com/Homebrew/linuxbrew.git ~/.linuxbrew

    See more info: http://brew.sh/linuxbrew/

     Install hub
        - $ brew install hub

        - Aliasing (if you want):
            Place this command in your .bash_profile:
                - $ vim ~/.bash_profile
                eval "$(hub alias -s)"

            Note: You can also add to .profile file.

    See more info: https://github.com/github/hub or https://hub.github.com/

    Scripts from gist-vauxoo
    - $ git clone git@github.com:vauxoo-dev/gist-vauxoo.git

How to use
        Copy the required files to your folder from gist-vauxoo to your project folder:
        $ cp DescriptionToReadmeMD.py /home/odoo/projects/demo-gitflow
        $ cp md2rst.py /home/odoo/projects/demo-gitflow
        Execute the script file in your currently project folder:
        e. g.
        $ mkdir -p /home/odoo/projects/demo-gitflow
        $ cd /home/odoo/projects/demo-gitflow
        $ ./autopep8-github.py git@github.com:Vauxoo/demo-gitflow.git git@github.com:vauxoo-dev/demo-gitflow.git KarenKawaii --pullrequest '''  # noqa
'''
usage: autopep8-github.py [-h] [--pullrequest] [--no-pullrequest]
                          remotebase remotedev author

positional arguments:
  remotebase        The names of the git remote base to use. Use remote bases
                    names comma separated without spaces e.g.
                    'git@github.com:Vauxoo/maintainer-tools.git,
                    git@github.com:Vauxoo/demo-gitflow.git'
  remotedev         The names of the git developer remote to use. Use dev
                    remote names comma separated without spaces. e.g.
                    'git@github.com:vauxoo-dev/maintainer-tools.
                    git,git@github.com:vauxoo-dev/demo-gitflow.git'
  author            Name from the author. Username from Github.

optional arguments:
  -h, --help        show this help message and exit
  --pullrequest     Enable pull request.
  --no-pullrequest  Disable pull request.

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
        # print repo_name

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
        # print cmd

        cmd = ['git', '--git-dir=' + os.path.join(git_repo_path, '.git'),
               'remote', 'add', org_dev, repodevs[cont]]
        subprocess.call(cmd)
        # print cmd
        cont = cont + 1

        # Bringing all changes from the remote repo
        cmd = ['git', '--git-dir=' + os.path.join(git_repo_path, '.git'),
               'fetch', '--all']
        subprocess.call(cmd)
        # print cmd

        cmd = ['git', 'branch', '-a']
        subprocess.call(cmd)

        # Create branch
        # Watch out with this!
        # if you include --git-dir, the files
        # will be added to your current folder,
        # not to the specific --git-dir
        # Please use it inside of the folder you want to pull
        cmd = ['git', '--git-dir=' + git_repo_path_branch, 'checkout',
               '-b', '8.0-standardize-' + repo_name + '-pr1-dev-' +
               author.lower(), '--track', 'vauxoo/8.0']
        subprocess.call(cmd)

        # README.rst

        # Add missing README.md from description in the __openerp__.py file
        # If README.rst exists, skip this command.
        files = os.listdir(git_repo_path)
        print files
        for element in files:
            if os.path.isdir(element) and element != '__unported__':
                if os.path.exists(os.path.join(git_repo_path,
                                               element, 'README.rst')):
                    print "It doesn't need to add README.md file"
                else:
                    cmd = ['python', 'DescriptionToReadmeMD.py', '-p',
                           os.path.join(git_repo_path, element)]
                    subprocess.call(cmd)

        # Listing README.md files in the current project folder.
        files = os.listdir(git_repo_path)
        print files
        for element in files:
            if os.path.isdir(element) and element != '__unported__':
                # Git command to add new README.md files
                cmd = ['git', 'add',
                       os.path.join(git_repo_path, element, 'README.md')]
                print cmd
                subprocess.call(cmd)
                # Convert README.md files to README.rst files
                cmd = ['python', 'md2rst.py', '-p', element]
                subprocess.call(cmd)

        # Checking git status to check if the README.md files are added.
        cmd = ['git', 'status']
        subprocess.call(cmd)

        # Convert README.md files to README.rst files
        # cmd = ['python', 'md2rst.py', '-p', git_repo_path]
        # subprocess.call(cmd)

        # Modify with oca-autopep8.
        # Disable because in ocations causes more troubles with lines to long.
        # cmd = ['oca-autopep8', '-ri', git_repo_path]
        # subprocess.call(cmd)

        # Output of rgrep command to do CamelCase manually to modules
        # that require it.
        os.system('rgrep -n addons . --include=*.py | grep from | grep -v decimal_precision | grep -v amount_to_text_es_mx | grep -v report_webkit | grep -v mute_logger')  # noqa

        # Modify wih oca-autopep8, delete vim comment,
        # Change coding comment and insert missing comment.
        cmd = ['oca-autopep8', '-ri',
               '--select=CW0001,CW0002,W391,CW0003,CW0004',
               git_repo_path]
        subprocess.call(cmd)

        # Remove magic comment interpreter
        os.system("find . -type f -name '*.py' -exec sed -i '/#!\/usr\/bin\/python/d' {} \;")  # noqa

        # Remove execute permissions
        os.system('find . -type f -name "*.py" -exec chmod -x {} \;')

        # Remove active key
        os.system("find . -type f -name '__openerp__.py' -exec sed -i '/'active'/d' {} \;")  # noqa

        # Remove active key 2
        os.system('find . -type f -name "__openerp__.py" -exec sed -i "/"active"/d" {} \;')  # noqa

        # Checking changes in repo
        cmd = ['git', 'diff']
        subprocess.call(cmd)

        # Ignore __unported__ folder to commit
        cmd = ['git', 'checkout', '--', '__unported__/']
        subprocess.call(cmd)

        # Checking files before commit
        cmd = ['git', 'status']
        subprocess.call(cmd)

        # Make a commit
        cmd = ['git', 'commit', '--author', author, '-am',
               "[REF] " + repo_name + ": Standardize project with odoo guidelines."]  # noqa
        subprocess.call(cmd)
        # print cmd

        # Git push
        cmd = ['git', 'push', org_dev,
               '8.0-standardize-' + repo_name + '-pr1-dev-' + author.lower()]
        subprocess.call(cmd)
        # print cmd

        # Creating pull request
        if pull_request:
            cmd = ['hub', 'pull-request', '-o', '-b', org + '/' + repo_name +
                   ':' + series[0], '-h', org_dev + ':' + '8.0-standardize-'
                   + repo_name + '-pr1-dev-' + author.lower()]
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
                        help="Name from the author. Username from Github.",
                        type=str)

    parser.add_argument("--pullrequest",
                        dest="pull_request",
                        action='store_true',
                        help="Enable pull request.")

    parser.add_argument("--no-pullrequest",
                        dest="pull_request",
                        action='store_false',
                        help="Disable pull request.")

    parser.set_defaults(pull_request=False)
    args = parser.parse_args()

    # Split the string into a list.
    remote_base_list = args.remotebase.split(',')
    remote_dev_list = args.remotedev.split(',')
    create_repo_branches(remote_base_list,
                         remote_dev_list,
                         args.author,
                         args.pull_request)

if __name__ == '__main__':
    main()
