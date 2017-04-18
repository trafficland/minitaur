## deployment
Deployment is handled by the python tool http://www.fabfile.org/.

You will create a virtual environment using virtualenv http://docs.python-guide.org/en/latest/dev/virtualenvs/.

You will need the Development Tools and python-devel packages installed on the CentOS instance.

The RPM that is built during the deployment process must be built on a Linux host.  We use CentOS.

If you are not running a CentOS host natively you will need a virtual machine with CentOS installed.

Once you have a base CentOS installation you must prepare it to use the deployment tools.  The following link will walk you through setting up your Linux host.
 
https://www.digitalocean.com/community/tutorials/how-to-set-up-python-2-7-6-and-3-3-3-on-centos-6-4

Once you have the deployment tools installed, deployment is easy.

From the minotaur source code directory.

```
cd deploy
virtualenv minotaur_deploy
source minotaur_deploy/bin/activate (you can deactivate using the deactivate command)
```

Use the requirements.txt file located in the ../deploy directory to install all needed dependencies.

```
pip install -r requirements.txt
```

Once your virtual environment is installed run fabric tasks as follows.

```
fab <task> --hosts=<host0,host1,...,hostx> --set enviro=[dev | stage | prod] --user=<username> -I
```

Deploy tasks:

deploy_full 	- (Default) - Test, Build, Deploy and start the imageengine service on the remote host. 

deploy_no_build - Deploy and start the minotaur service on the remote host.

deploy_no_start - Test, Build, and Deploy the minotaur service to the remote host.

deploy_no_test  - Build, deploy and start the minotaur service on the remote host. Skip the unit tests.


E.g. Run the following to deploy Minotaur to stage.
```
deploy --hosts=minotaur-1.stage.tl.com --set enviro=stage --user=<username> -I
```