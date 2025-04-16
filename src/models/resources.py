from pulumi.output import Output
from pulumi import ResourceOptions
from pulumi_aws.s3 import BucketWebsiteArgs
from pydantic import BaseModel
from typing import Union
from enum import Enum


class TableBillingEnum(str, Enum):
    PROVISIONED = "PROVISIONED"
    PAY_PER_REQUEST = "PAY_PER_REQEUST"


class Route53RecordTypeEnum(str, Enum):
    CNAME = "CNAME"
    TXT = "TXT"
    A = "A"


class CloudFrontDistributionPriceClassEnum(str, Enum):
    PriceClass_100 = "PriceClass_100"
    PriceClass_200 = "PriceClass_200"


class S3BucketCreateModel(BaseModel):
    resource_name: str
    bucket: str
    acl: str = "public-read"
    website: BucketWebsiteArgs | None = None

    class Config:
        arbitrary_types_allowed = True


class DynamoDbTableCreateModel(BaseModel):
    table_name: str
    attributes: list[dict[str, str]]
    hash_key: str
    range_key: str | None = None
    billing_mode: TableBillingEnum = TableBillingEnum.PROVISIONED
    read_capacity: int | None = 5
    write_capacity: int | None = 5


class CertificateCreateModel(BaseModel):
    resource_name: str
    domain_name: str
    validation_method: str = "DNS"
    opts: ResourceOptions | None = None

    class Config:
        arbitrary_types_allowed = True


class CertificateValidateModel(BaseModel):
    resource_name: str
    certificate_arn: Output[str]
    validation_record_fqdns: list[Output[str]]
    opts: ResourceOptions | None = None

    class Config:
        arbitrary_types_allowed = True


class Route53RecordCreateModel(BaseModel):
    resource_name: str
    name: Union[str, Output[str]]
    type: Route53RecordTypeEnum = Route53RecordTypeEnum.A
    records: list[Output[str]] | None = None
    aliases: list[dict[Output[str], Output[str]]] | None = None
    zone_id: str
    ttl: int | None = None

    class Config:
        arbitrary_types_allowed = True


Route53RecordCreateModel.model_rebuild()


class CloudFrontDistributionCreateModel(BaseModel):
    resource_name: str
    aliases: list[str]
    logging_bucket: Output | None = None
    website_bucket_arn: Output
    website_bucket_endpoint: Output
    certificate_arn: Output | None = None
    price_class: CloudFrontDistributionPriceClassEnum = (
        CloudFrontDistributionPriceClassEnum.PriceClass_100
    )
    enabled: bool | None = True
    wait_for_deployment: bool | None = False
    cache_min_ttl: int | None = 0
    cache_max_ttl: int | None = 3600
    cache_default_ttl: int | None = 600

    class Config:
        arbitrary_types_allowed = True
