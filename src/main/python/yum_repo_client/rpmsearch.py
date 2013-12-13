from yum_repo_client.rpmfile import RpmFile
import rpm
import re

class RpmSearch():
  def search_rpms_with_name(self, rpm_name, files, sort_desc = False):
    matcher = re.compile(rpm_name)
    found_rpms = [RpmFile(rpm_file['filename']) for rpm_file in files if matcher.search(rpm_file['filename'])]

    found_rpms.sort(cmp=self._compare_rpms_by_version, reverse=sort_desc)

    return found_rpms

  def _compare_rpms_by_version(self, rpm_file1, rpm_file2):
    return rpm.labelCompare(('1', rpm_file1.version, rpm_file1.release), ('1', rpm_file2.version, rpm_file2.release))
