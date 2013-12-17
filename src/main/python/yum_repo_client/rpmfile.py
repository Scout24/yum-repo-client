class RpmFile():
    def __init__(self, file_name):
        if not file_name.endswith('.rpm') or file_name.count('-') < 2 or file_name.count('.') < 2:
            raise Exception('RPM file name "%s" does not follow the naming pattern "name-version-release.arch.rpm"' % file_name)

        rpm_parts = file_name.rsplit('.', 2)

        rpm_name_parts = rpm_parts[0].rsplit('-', 2)

        self.filename = file_name
        self.arch = rpm_parts[1]
        self.name = rpm_name_parts[0]
        self.version = rpm_name_parts[1]
        self.release = rpm_name_parts[2]