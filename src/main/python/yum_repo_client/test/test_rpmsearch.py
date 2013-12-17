import unittest
from yum_repo_client.rpmsearch import RpmSearch

class TestRpmSearch(unittest.TestCase):
  
    def setUp(self):
        self.rpm_search = RpmSearch()
    
    def test_find_rpm(self):
        files = [{'filename': 'foo-12.3-2.noarch.rpm'},
                 {'filename': 'foo-bar-12.3-2.noarch.rpm'},
                 {'filename': 'foo-bar-plugin-12.3-2.noarch.rpm'},
                 {'filename': 'foo-rab-12.3-2.noarch.rpm'}]
      
        found_rpms = self.rpm_search.search_rpms_with_name('bar', files)
      
        self._assert_found_rpms_list(found_rpms, [
            'foo-bar-12.3-2.noarch.rpm',
            'foo-bar-plugin-12.3-2.noarch.rpm'])
    
    def test_sort_found_rpms_asc(self):
        files = [{'filename': 'foo-12.3-2.noarch.rpm'},
                 {'filename': 'foo-bar-12.3-2.noarch.rpm'},
                 {'filename': 'foo-bar-12.3-3.noarch.rpm'},
                 {'filename': 'foo-bar-12.4-2.noarch.rpm'}]
      
        found_rpms = self.rpm_search.search_rpms_with_name('bar', files)
    
        self._assert_found_rpms_list(found_rpms, [
          'foo-bar-12.3-2.noarch.rpm',
          'foo-bar-12.3-3.noarch.rpm',
          'foo-bar-12.4-2.noarch.rpm'])
    
    def test_sort_found_rpms_desc(self):
        files = [{'filename': 'foo-12.3-2.noarch.rpm'},
                 {'filename': 'foo-bar-12.3-2.noarch.rpm'},
                 {'filename': 'foo-bar-12.3-3.noarch.rpm'},
                 {'filename': 'foo-bar-12.4-2.noarch.rpm'}]
      
        found_rpms = self.rpm_search.search_rpms_with_name('bar', files, True)
      
        self._assert_found_rpms_list(found_rpms, [
          'foo-bar-12.4-2.noarch.rpm',
          'foo-bar-12.3-3.noarch.rpm',
          'foo-bar-12.3-2.noarch.rpm'])
      
    def test_sort_by_name_and_version(self):
        files = [{'filename': 'foo-12.3-2.noarch.rpm'},
                 {'filename': 'foo-bar-12.3-2.noarch.rpm'},
                 {'filename': 'foo-bar-plugin-12.3-3.noarch.rpm'},
                 {'filename': 'foo-bar-12.4-2.noarch.rpm'}]
      
        found_rpms = self.rpm_search.search_rpms_with_name('bar', files)
      
        self._assert_found_rpms_list(found_rpms, [
          'foo-bar-12.3-2.noarch.rpm', 
          'foo-bar-12.4-2.noarch.rpm', 
          'foo-bar-plugin-12.3-3.noarch.rpm'])
      
    def test_sort_by_name_and_version_desc(self):
        files = [{'filename': 'foo-12.3-2.noarch.rpm'},
                 {'filename': 'foo-bar-12.3-2.noarch.rpm'},
                 {'filename': 'foo-bar-plugin-12.3-3.noarch.rpm'},
                 {'filename': 'foo-bar-12.4-2.noarch.rpm'}]
      
        found_rpms = self.rpm_search.search_rpms_with_name('bar', files, True)
      
        self._assert_found_rpms_list(found_rpms, [
          'foo-bar-plugin-12.3-3.noarch.rpm',
          'foo-bar-12.4-2.noarch.rpm', 
          'foo-bar-12.3-2.noarch.rpm'])
      
    def _assert_found_rpms_list(self, actual, expected):
        actual_names = [x.filename for x in actual]
      
        self.assertEqual(len(actual), len(expected))
        for i in range(0, len(expected)):
            self.assertEqual(actual_names[i], expected[i], '\nExpected list:\t%s\nGot:\t\t%s' % (expected, actual_names))
    