from . import indexes
from . import messages
from grow.pods import pods
from grow.pods import storage
import unittest


class IndexTest(unittest.TestCase):

  def setUp(self):
    self.pod = pods.Pod('grow/pods/testdata/pod/', storage=storage.FileStorage)

  def assertFilePathsEqual(self, my_file_messages, their_file_messages):
    for i, file_message in enumerate(my_file_messages):
      self.assertEqual(file_message.path, their_file_messages[i].path)

  def test_diff(self):
    my_index = indexes.Index.create({
      '/file.txt': 'test',
      '/file2.txt': 'test',
      '/foo/file.txt': 'test',
      '/foo/file.txt': 'test',
    })
    their_index = indexes.Index.create({
      '/file2.txt': 'change',
      '/foo/file.txt': 'test',
      '/foo/file.txt': 'test',
      '/bar/new.txt': 'test',
    })
    expected = messages.DiffMessage(
        adds=[messages.FileMessage(path='/file.txt')],
        edits=[messages.FileMessage(path='/file2.txt')],
        deletes=[messages.FileMessage(path='/bar/new.txt')],
        nochanges=[messages.FileMessage(path='/foo/file.txt')],
    )
    diff = indexes.Diff.create(my_index, their_index)
    self.assertFilePathsEqual(expected.adds, diff.adds)


if __name__ == '__main__':
  unittest.main()

