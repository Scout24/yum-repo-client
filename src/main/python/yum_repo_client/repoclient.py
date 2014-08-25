import httplib
from dummy_thread import exit
import string
import base64
import urllib
import getpass

import pycurl


try:
    from html2text import html2text
except ImportError:
    html2text = lambda html: html
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class RepoException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

def _render(response):
    return html2text(response)

class HttpClient(object):
    USER_AGENT = 'repoclient/1.0'

    username = None
    password = None
    message = None

    def __init__(self, hostname, port, context=None, message=None):
        self.hostname = hostname
        self.port = port
        self.message = message
        self.context = '' if not context or context == '/' else context
        self._add_leading_context_slash_if_needed()

    def _add_leading_context_slash_if_needed(self):
        if self.context and not self.context.startswith('/'):
            self.context = "/%s" % self.context

    def queryStatic(self, params):
        urlparams = urllib.urlencode(params)
        response = self.doHttpGet('/repo.txt?%s' % urlparams)
        self.assertResponse(response, httplib.OK)
        return response

    def queryVirtual(self, params):
        urlparams = urllib.urlencode(params)
        response = self.doHttpGet('/repo/virtual.txt?' + urlparams)
        self.assertResponse(response, httplib.OK)
        return response

    def createStaticRepo(self, reponame):
        response = self.doHttpPost('/repo/', "name=" + reponame)
        self.assertResponse(response, httplib.CREATED)
        return response

    def delete_static_repo(self, reponame):
        response = self.doHttpDelete('/repo/%s' % reponame)
        self.assertResponse(response, httplib.NO_CONTENT)
        return response

    def untagRepo(self, reponame, tag):
        response = self.doHttpDelete('/repo/' + reponame + '/tags/' + tag)
        self.assertResponse(response, httplib.NO_CONTENT)
        return response

    def tagRepo(self, reponame, tag):
        response = self.doHttpPost('/repo/' + reponame + '/tags/', "tag=" + tag)
        self.assertResponse(response, httplib.CREATED)
        return response

    def tagList(self, reponame):
        response = self.doHttpGet('/repo/' + reponame + '/tags/')
        self.assertResponse(response, httplib.OK)
        return response

    def uploadRpm(self, reponame, rpm_file_name):
        c = pycurl.Curl()
        response_buffer = StringIO()
        c.setopt(c.WRITEFUNCTION, response_buffer.write)
        c.setopt(c.POST, 1)
        url = "http://%s:%d/%s/repo/%s/" % (self.hostname, self.port, self.context, reponame)
        c.setopt(c.URL, url)
        c.setopt(c.HTTPPOST, [("rpmFile", (c.FORM_FILE, rpm_file_name))])
        c.setopt(pycurl.HTTPHEADER, ['User-Agent: ' + self.USER_AGENT, 'Username: ' + self.get_user_name()])
        if self.username is not None:
            c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
            c.setopt(pycurl.USERPWD, '%s:%s' % (self.username, self.password))

        c.perform()
        returncode = c.getinfo(pycurl.HTTP_CODE)
        c.close()

        response_text = _render(response_buffer.getvalue())
        response_buffer.close()

        if returncode != httplib.CREATED:
            raise RepoException("Upload failed.\nServer says: {0}".format(response_text))

    def deleteSingleRpm(self, reponame, rpm_file_name):
        response = self.doHttpDelete('/repo/' + reponame + '/' + rpm_file_name)
        self.assertResponse(response, httplib.NO_CONTENT)
        return response

    def generateMetadata(self, reponame):
        response = self.doHttpPost('/repo/' + reponame + '/repodata')
        self.assertResponse(response, httplib.CREATED)
        return response

    def createVirtualRepo(self, virtual_reponame, destination_reponame):
        post_data = 'name=' + virtual_reponame + "&destination=" + destination_reponame
        response = self.doHttpPost('/repo/virtual/', post_data)
        self.assertResponse(response, httplib.CREATED)
        return response

    def createLinkToVirtualRepo(self, virtual_reponame, destination_virtual_reponame):
        return self.createVirtualRepo(virtual_reponame, 'virtual/' + destination_virtual_reponame)

    def createLinkToStaticRepo(self, virtual_reponame, static_reponame):
        return self.createVirtualRepo(virtual_reponame, 'static/' + static_reponame)

    def deleteVirtualRepo(self, virtual_reponame):
        response = self.doHttpDelete('/repo/virtual/' + virtual_reponame)
        self.assertResponse(response, httplib.NO_CONTENT)
        return response

    def propagate_rpm(self, fromrepo, rpm_arch_slash_name, torepo):
        post_data = 'source=' + fromrepo + "/" + rpm_arch_slash_name + "&destination=" + torepo
        response = self.doHttpPost('/propagation/', post_data)
        self.assertResponse(response, httplib.CREATED)
        return response

    def propagate_repo(self, source_repository, destination_repository):
        post_data = 'source=' + source_repository + "&destination=" + destination_repository
        response = self.doHttpPost('/repo-propagation/', post_data)
        self.assertResponse(response, httplib.CREATED)
        return response

    def get_archs(self, reponame):
        response = self.doHttpGet('/repo/' + reponame + '.json')
        self.assertResponse(response, httplib.OK)
        return response

    def get_files(self, reponame, arch):
        response = self.doHttpGet('/repo/' + reponame + '/' + arch + '.json')
        self.assertResponse(response, httplib.OK)
        return response

    def doHttpPost(self, extPath, postdata='', headers=None):
        if postdata and self.message:
            postdata += '&YRS_MESSAGE=' + str(self.message)
        if not headers:
            headers = {}
        headers['User-Agent'] = self.USER_AGENT
        headers['Username'] = self.get_user_name()

        if self.username is not None:
            auth = 'Basic ' + string.strip(base64.encodestring(self.username + ':' + self.password))
            headers['Authorization'] = auth
        try:
            httpServ = httplib.HTTPConnection(self.hostname, self.port)
            httpServ.connect()
            httpServ.request('POST', self.context + extPath, postdata, headers)
            response = httpServ.getresponse()
            return response
        except httplib.HTTPException:
            print "ERROR! Looks like the server is not running on " + self.hostname
            exit()

    def doHttpDelete(self, extPath):
        headers = {'User-Agent': self.USER_AGENT, 'Username': self.get_user_name()}

        if self.username is not None:
            auth = 'Basic ' + string.strip(base64.encodestring(self.username + ':' + self.password))
            headers['Authorization'] = auth

        try:
            httpServ = httplib.HTTPConnection(self.hostname, self.port)
            httpServ.request('DELETE', self.context + extPath, None, headers)
            response = httpServ.getresponse()
            return response
        except httplib.HTTPException:
            print "ERROR! Looks like the server is not running on " + self.hostname
            exit()

    def doHttpGet(self, extPath):
        headers = {'User-Agent': self.USER_AGENT, 'Username': self.get_user_name()}

        if self.username is not None:
            auth = 'Basic ' + string.strip(base64.encodestring(self.username + ':' + self.password))
            headers['Authorization'] = auth

        try:
            httpServ = httplib.HTTPConnection(self.hostname, self.port)
            httpServ.request('GET', self.context + extPath, None, headers)
            response = httpServ.getresponse()
            return response
        except httplib.HTTPException:
            print "ERROR! Looks like the server is not running on " + self.hostname
            exit()

    def assertResponse(self, response, expectedStatus):
        if response.status != expectedStatus:
            raise RepoException(
                "ERROR: Got unexpected status code {0} ({1}). Expected {2}.\nThe server said:\n{3}".format(
                response.status, response.reason, expectedStatus, _render(response.read())))

    def get_user_name(self):
        return self.username if self.username is not None else getpass.getuser()
