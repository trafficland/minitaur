import os
from os.path import join
import fnmatch

from fabric.network import ssh
from fabric.api import local, run, put, env, sudo, task, settings
from fabric.decorators import runs_once
from mako.template import Template
from fabric.contrib.console import confirm
from deploy_context import *

ssh.util.log_to_file("paramiko.log", 10)

env.use_ssh_config = True

DEPLOY_DIR = os.getcwd()
WORKSPACE_DIR = join(DEPLOY_DIR, "config_files/workspace")
ROOT_DIR = os.path.dirname(DEPLOY_DIR)
os.chdir(ROOT_DIR)

SERVICE_NAME = "minotaur"
PACKAGE_DIR = "target/rpm/RPMS/noarch"

REMOTE_ROOT = join("/opt/trafficland", SERVICE_NAME)
REMOTE_CONF = join(REMOTE_ROOT, "conf")


def result_handler(result, message, return_code=0):
    if result.failed or result.return_code != return_code:
        print result
        raise Exception()
    else:
        print message


@task(default=True)
def deploy_full():
    """
       (Default) - Test, Build, Deploy and start the minotaur service on the remote host. Usage fab -H [remote host to deploy to] -u [your name on remote host] --set enviro=[dev or staging or production,no_build,no_test,no_start]
    """
    print("Deploying to {enviro}".format(enviro=env.enviro))
    check_hosts()
    unit_test()
    build_rpm()
    deploy_rpm_to_remotes()
    build_config_files()
    copy_config_files_to_remotes()
    start_service()


@task
def deploy_no_build():
    """
       (Default) - Test, Build, Deploy and start the minotaur service on the remote host. Usage fab -H [remote host to deploy to] -u [your name on remote host] --set enviro=[dev or staging or production,no_build,no_test,no_start]
    """
    print("Deploying to {enviro}".format(enviro=env.enviro))
    check_hosts()
    deploy_rpm_to_remotes()
    build_config_files()
    copy_config_files_to_remotes()
    start_service()


@task
def deploy_no_start():
    """
        Test, Build, and Deploy the minotaur service to the remote host.
    """
    print("Deploying to {enviro}".format(enviro=env.enviro))
    check_hosts()
    unit_test()
    build_rpm()
    deploy_rpm_to_remotes()
    build_config_files()
    copy_config_files_to_remotes()


@task
def deploy_no_test():
    """
        Build, deploy and start the minotaur service on the remote host. Skip the unit tests.
    """
    print("Deploying to {enviro}".format(enviro=env.enviro))
    check_hosts()
    build_rpm()
    deploy_rpm_to_remotes()
    build_config_files()
    copy_config_files_to_remotes()
    start_service()


@runs_once
def build_rpm():
    print "********** RUNS ONLY ONCE ********"
    with settings(warn_only=True):
        result = local("./sbt rpm:packageBin", capture=True)
    result_handler(result, "packaged")


def deploy_rpm_to_remotes():
    full_package_path = os.path.join(ROOT_DIR, PACKAGE_DIR)
    rpm_path = None
    rpm = None

    for file in os.listdir(full_package_path):
        if fnmatch.fnmatch(file, '*.noarch.rpm'):
            rpm = file
            rpm_path = os.path.join(full_package_path, file)

    print("RPM located at {path}".format(path=rpm_path))

    # Warn only in case this is a first time run
    sudo("rpm -e {service_name}".format(service_name=SERVICE_NAME), warn_only=True)
    print("Putting RPM")
    put(rpm_path, "/tmp")
    sudo("rpm -ivh /tmp/{rpm}".format(rpm=rpm))


def copy_config_files_to_remotes():
    files = os.path.join(DEPLOY_DIR, "config_files/workspace") + "/*"
    common_files = os.path.join(DEPLOY_DIR, "config_files/common") + "/*"
    print "Putting  {files}".format(files=files)
    put(common_files, REMOTE_CONF, use_sudo=True)
    put(files, REMOTE_CONF, use_sudo=True)


@runs_once
def unit_test():
    print "********** RUNS ONLY ONCE ********"
    with settings(warn_only=True):
        result = local("./sbt test", capture=True)
    result_handler(result, "tested")


def start_service():
    sudo("service minotaur start", warn_only=True)


def check_hosts():
    run("hostname")

    if not os.path.exists(WORKSPACE_DIR):
        os.makedirs(WORKSPACE_DIR)


def get_template(template_name):
    template = join(DEPLOY_DIR, "config_files/templates/{template}.template".format(template=template_name))
    return Template(filename=template)


def template_writer(template_name, rendered):
    rendered_file = join(DEPLOY_DIR, "config_files/workspace/{template}".format(template=template_name))
    print("Template rendered")
    with open(rendered_file, "w") as text_file:
        text_file.write(rendered)


@task
def build_config_files():
    template = get_template("prod.conf")
    rendered = template.render(imageengine_templateurl=IMAGEENGINE_TEMPLATEURL)
    template_writer("prod.conf", rendered)

    template = get_template("logback.xml")
    rendered = template.render(debug_level=DEBUG_LEVEL)
    template_writer("logback.xml", rendered)
