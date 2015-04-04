#!/usr/bin/env python

import argparse
import os
import subprocess

from oca_projects import url


def get_project_path(project_name, org_name, branch=None, base_path='/tmp/'):
    project_path = org_name + '__' + project_name
    if branch:
        project_path += '__' + branch.split('/')[-1]
    if base_path:
        project_path = os.path.join(base_path, project_path)
    return project_path


# def git_cmd(project_name, org_name, subcmd, base_path=None):
#     cmd = ['git', '--git-dir=' + \
#            os.path.join(get_project_path( \
#             project_name, org_name), '.git')] \
#            + subcmd
#     return subprocess.check_output(cmd)


def get_all_branches(project_path, remote='origin'):
    cmd = ['git', '--git-dir=' +
           os.path.join(project_path, '.git'),
           'branch', '-r']
    branches_str = subprocess.check_output(cmd)
    branches = [branch.strip() for branch in branches_str.split('\n')][:-1]
    #import pdb;pdb.set_trace()
    """
    for branch in branches:
        cmd = ['git', '--git-dir=' +
               os.path.join(
                   get_project_path(
                      project_name, org_name), '.git'),
               'branch', '--track', branch]
        subprocess.call(cmd)
    """
    return branches


def clone(project_name, org_name, branch=None, protocol='git'):
    if not os.path.isdir(os.path.join(project_name, '.git')):
        cmd = ['git', 'clone',
               url(project_name, org_name=org_name, protocol=protocol),
               get_project_path(project_name, org_name, branch)]
        if branch:
            cmd = cmd + ['-b', branch]
        subprocess.call(cmd)
        return 1
    return -1


def decode_utf(field):
    try:
        return field.decode('utf-8')
    except UnicodeDecodeError:
        return ''


def ls_ref(project_path):
    fields = ['refname']
    fmt = "%00".join(["%("+field+")" for field in fields])
    cmd_refs = ['for-each-ref', '--format', fmt, '--sort=refname',
                'refs/heads']
    cmd = ['git',
           '--git-dir=%s' % os.path.join(project_path, '.git')] + cmd_refs
    git_refs = subprocess.check_output(cmd)
    git_refs = git_refs.strip()
    refs = [[decode_utf(field) for field in line.split('\x00')]
            for line in git_refs.split('\n')]
    #  Filter just refs remotes (not current branch) and use just branch name
    refs = [ref[0].split('/')[-1] for ref in refs if ref[0].count('/') == 3]
    return refs


def git_checkout(project_path, branch_sha, new_branch_name=None):
    if new_branch_name is None:
        new_branch_name = branch_sha
    cmd = ['git', '--git-dir=%s' % os.path.join(project_path, '.git'),
           'checkout', '-f', '-b', new_branch_name, '--track', branch_sha]
    print ' '.join(cmd)
    subprocess.call(cmd)
    cmd = ['git', '--git-dir=%s' % os.path.join(project_path, '.git'),
           'stash']
    subprocess.call(cmd)
    return True


def run_output(cmd, cwd=None):
    print "cmd", ' '.join(cmd), "in", cwd
    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        cwd=cwd).communicate()[0]


def git_rm_path_log(project_path, path_to_remove):
    cmd = ['git', 'filter-branch', '-f', '--tree-filter',
           'rm -rf %s' % (path_to_remove), "HEAD"]
    return run_output(cmd, cwd=project_path)


def rm_path_ang_log(project_name, org_name, paths_to_remove):
    clone(project_name, org_name)
    project_path = get_project_path(project_name, org_name)
    branches = get_all_branches(project_path)
    #import pdb;pdb.set_trace
    for branch in branches:
        branch_sp = branch.split('/')[-1]
        clone(project_name, org_name, branch_sp)
        project_branch_path = get_project_path(project_name, org_name, branch_sp)
        for path_to_remove in paths_to_remove:
            git_rm_path_log(project_branch_path, path_to_remove)
        #get_project_path(project_name, org_name, branch)
        #git_checkout(project_path, branch, branch.split('/')[-1])
        """
        git_checkout(project_path, branch, branch.split('/')[-1])
        for path_to_remove in paths_to_remove:
            git_rm_path_log(project_path, path_to_remove)
            import pdb;pdb.set_trace()
        """

    """
    refs = ls_ref(project_path)
    for ref in refs:
        import pdb;pdb.set_trace()
        git_checkout(project_path, ref, ref + '-rm-path')
        for path_to_remove in paths_to_remove:
            git_rm_path_log(project_path, path_to_remove)
    print "Later execute: git push --all -u"
    """


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-name", dest="project_name",
                        help="Specify short name of project."
                        "Without organization name",
                        nargs=1, default=None, required=True)
    parser.add_argument("--organization-name", dest="org_name",
                        help="Specify organization name.",
                        nargs=1, default=None, required=True)
    parser.add_argument("--paths-to-remove", dest="paths_to_rm",
                        help="Specify paths to remove from git log."
                             "Split with commas.",
                        nargs=1, default=None, required=True)
    args = parser.parse_args()
    project_name = args.project_name and args.project_name[0] or None
    org_name = args.org_name and args.org_name[0] or None
    paths_to_rm_str = args.paths_to_rm and args.paths_to_rm[0] or None
    paths_to_rm = paths_to_rm_str.split(',')
    print org_name, "/", project_name, "rm", paths_to_rm
    rm_path_ang_log(
        project_name=project_name,
        org_name=org_name,
        paths_to_remove=paths_to_rm)


if __name__ == '__main__':
    main()
