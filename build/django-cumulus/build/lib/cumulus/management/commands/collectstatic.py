import hashlib

from django.contrib.staticfiles.management.commands import collectstatic

from cumulus.storage import CloudFilesStorage

class Command(collectstatic.Command):

    def delete_file(self, path, prefixed_path, source_storage):
        """
        Checks if the target file should be deleted if it already exists
        """
        if isinstance(self.storage, CloudFilesStorage):
            if self.storage.exists(prefixed_path):
                try:
                    etag = self.storage._get_cloud_obj(prefixed_path).etag
                    digest = "{0}".format(hashlib.md5(source_storage.open(path).read()).hexdigest())
                    print etag, digest
                    if etag == digest:
                        self.log(u"Skipping '{0}' (not modified based on file hash)".format(path))
                        return False
                except:
                    raise
        return super(Command, self).delete_file(path, prefixed_path, source_storage)
