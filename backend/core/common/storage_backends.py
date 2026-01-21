"""
AWS S3 storage backends.
"""
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """S3 storage for media files (documents, images, etc.)."""
    location = 'media'
    file_overwrite = False
    default_acl = 'private'
