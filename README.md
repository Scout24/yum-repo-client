# yum-repo-client
===============

## Aim
'yum-repo-client' is a command line interface for interacting with the yum-repo-server
The aim is to provide a command line wrapper for every functionality the yum-repo-server provides so you don't have to fiddle with REST requests.
This is especially good for automations that can run command line tools because you can modify the yum-repo-server as you wish without breaking your automation (provided you include the modifications in the yum-repo-client).

## Features
The yum-repo-client currently supports
* Remote repository creation and deletion
* RPM upload and remote deletion
* Virtual repository creation, linking, redirection and deletion
* Optional authentication and yum-repo-server host parametrization
* RPM propagation
* Smart bash autocompletion

## Getting started
### Obtaining the yum-repo-client
The yum-repo-client comes bundled with the yum-repo-server.
Everything you need is located in the project subfolder 'client'.
### Building the yum-repo-client
First of all it is recommended to run the tests:
<code>
python setup.py test
</code>

These should always be successfull. 
#### Build RPM
Optionally after that you can run:
<code>
python setup.py bdist_rpm
</code>
to get an rpm of the yum-repo-client.
#### Build DEB
To build a DEB package first install python-stdeb and then run:
<code>
python setup.py --command-packages=stdeb.command bdist_deb
</code>
The resulting deb package will be in the `deb_dist` subfolder. Please keep in mind that in most cases it is not a good idea to build RPMs on Debian as the RPM dependencies can go horribly wrong. Creating Source RPMs should be less problematic.

### Installing the yum-repo-client
If you have built a rpm file in the step above, then you can install it as usual.

Without the rpm file you can install the yum-repo-client with:
<code>
python setup.py install
</code>
### Using the yum-repo-client
Simply call 
<code>repoclient</code> 
to display the help text that includes call syntax and operation description
### Setting the defaults
To set the default host and port used by the yum-repo-client, you need to edit (or create) the file `/etc/yum-repo-client.yaml`.
This file should contain the following entries :
`DEFAULT_HOST : localhost`
`DEFAULT_PORT : 8000`
The configuration above is for usage with the django development server (not for production use!).
