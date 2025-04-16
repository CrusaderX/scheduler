from pulumi_aws.s3 import Bucket, BucketObject
from pulumi import FileAsset, Resource, ResourceOptions
from mimetypes import guess_type

from utils import files_to_upload
from models.resources import S3BucketCreateModel


class AmazonServiceS3:
    @staticmethod
    def upload_to_bucket(
        parent: Resource, props: S3BucketCreateModel, root: str
    ) -> None:
        files = files_to_upload(root=root)

        assert files

        for key, relative_path in files.items():
            content_type, _ = guess_type(key)
            BucketObject(
                relative_path,
                key=relative_path,
                acl=props.acl,
                bucket=props.bucket,
                content_type=content_type,
                source=FileAsset(key),
                opts=ResourceOptions(parent=parent),
            )

    @staticmethod
    def create_bucket(props: S3BucketCreateModel) -> Bucket:
        return Bucket(**props.model_dump())
