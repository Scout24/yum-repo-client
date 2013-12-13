import unittest
from yum_repo_client.commands import QueryRpmCommand
from StringIO import StringIO

class TestQueryRpmCommand(unittest.TestCase):
  
  def setUp(self):
    self.output = StringIO()
    self.http_client_mock = HttpClientMock()
    self.command = QueryRpmCommand(self.output)
    self.command.httpClient = self.http_client_mock
    
    files = '[{"repo":"production", "filename":"a-a-a-12.2-15.noarch.rpm"},' + \
    '{"repo":"production", "filename":"a-a-a-12.3-15.noarch.rpm"},' + \
    '{"repo":"production", "filename":"a-a-b-12.2-15.noarch.rpm"},' + \
    '{"repo":"production", "filename":"b-a-a-12.2-15.noarch.rpm"},' + \
    '{"repo":"production", "filename":"b-a-b-12.2-15.noarch.rpm"}]'
    self.http_client_mock.files_for('production', 'noarch', files)
  
  def test_find_rpms(self):
    self.command.doRun(self._create_args('a-a', 'production', 'noarch'))
    
    self.assertEquals(
      'a-a-a-12.2-15.noarch.rpm\na-a-b-12.2-15.noarch.rpm\nb-a-a-12.2-15.noarch.rpm\na-a-a-12.3-15.noarch.rpm\n',
      self.output.getvalue())
  
  def test_sort_descending(self):
    self.command.doRun(self._create_args('a-a-a', 'production', 'noarch', 'desc'))
    
    self.assertEquals(
      'a-a-a-12.3-15.noarch.rpm\na-a-a-12.2-15.noarch.rpm\n',
      self.output.getvalue())
  
  def _create_args(self, rpm_name, repository, arch, sort=''):
    args = ArgumentMock(rpm_name, repository, arch, sort)
    return args

class ArgumentMock():
  def __init__(self, rpm_name, repository, arch, sort=''):
    self.rpm_name = rpm_name
    self.repository = repository
    self.arch = arch
    self.sort = sort
  
class HttpClientMock():
  def __init__(self):
    self.repositories = {}
  
  def files_for(self, repo, arch, items):
    key = '%s_%s' % (repo, arch)
    self.repositories[key] = items
  
  def get_files(self, repo, arch):
    key = '%s_%s' % (repo, arch)
    if self.repositories.has_key(key):
      return ResponseMock('{"items": %s}' % self.repositories[key])
    
    raise Exception('unexpected call for repository "%s" in arch "%s"' % (repo, arch))
  
class ResponseMock():
  def __init__(self, string):
    self.string = string
  
  def read(self):
    return self.string