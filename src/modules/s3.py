from pulumi_aws.s3 import Bucket, BucketWebsiteArgs, BucketObject
from pulumi import FileAsset, ResourceOptions
from typing import Optional
from mimetypes import guess_type

from utils import dict_to_simplenamespace, files_to_upload


class AmazonServiceS3:
    @staticmethod
    def upload_to_bucket(
        bucket: str, path: Optional[str] = ".", acl: Optional[str] = "public-read"
    ) -> None:
        files = files_to_upload(root=path)

        assert files

        for key, relative_path in files.items():
            content_type, _ = guess_type(key)
            BucketObject(
                relative_path,
                key=relative_path,
                acl=acl,
                bucket=bucket,
                content_type=content_type,
                source=FileAsset(key),
                opts=ResourceOptions(parent=bucket),
            )

    @staticmethod
    def create_bucket(props: dict) -> Bucket:
        props = dict_to_simplenamespace(props)

        if not hasattr(props, "website"):
            props.website = None
        else:
            props.website = BucketWebsiteArgs(
                index_document="index.html", error_document=""
            )

        return Bucket(
            props.name, bucket=props.name, acl=props.acl, website=props.website
        )
