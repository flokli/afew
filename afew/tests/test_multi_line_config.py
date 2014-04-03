import unittest

from afew.configparser import SafeConfigParser, RawConfigParser
from afew.filters.FolderNameFilter import FolderNameFilter

class TestMultiLineConfig(unittest.TestCase):
  def setUp (self):
    self.settings = SafeConfigParser()
    self.settings.optionxform = str
    self.notmuch_settings = RawConfigParser()

    self.test_config = """
[FolderNameFilter]
maildir_separator = /
folder_blacklist  = archive k b
folder_transforms = a:b
                    INBOX:inbox
                    "Deleted Messages":deleted
    """

    self.test_nm_config = """
[database]
path = /Mail

    """

  def test_multi_line_config (self):
    self.settings.read(self.test_config)
    self.notmuch_settings.read(self.test_nm_config)

    f = FolderNameFilter(None,
        self.settings.get('FolderNameFilter', 'folder_blacklist'),
        self.settings.get('FolderNameFilter', 'folder_transforms'),
        self.settings.get('FolderNameFilter', 'maildir_separator'),)
    tr = f._FolderNameFilter__folder_transforms

    self.assertEqual(tr['INBOX'], 'inbox')
    self.assertEqual(tr['Deleted Messages'], 'deleted')
