from pulumi.output import Output
from pydantic import BaseModel, Extra, validator, conint
from typing import Optional, Union, Dict
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


class DynamoDbTableCreateModel(BaseModel):
    table_name: str
    attributes: list[dict]
    hash_key: str
    range_key: Optional[str]
    billing_mode: TableBillingEnum = TableBillingEnum.PROVISIONED
    read_capacity: Optional[conint(gt=0, lt=40_000)] = 5
    write_capacity: Optional[conint(gt=0, lt=40_000)] = 5


class Route53RecordCreateModel(BaseModel):
    o: str
    name: object
    type: Route53RecordTypeEnum = Route53RecordTypeEnum.A
    records: Optional[list[Output]] = None
    aliases: Optional[
        list[dict[Optional[Union[str, Output]], Optional[Union[str, Output]]]]
    ] = None
    zone_id: str
    ttl: Optional[conint(lt=172_800)] = None

    class Config:
        arbitrary_types_allowed = True


class CloudFrontDistributionCreateModel(BaseModel):
    name: str
    aliases: list[str]
    logging_bucket: Optional[Output] = None
    website_bucket_arn: Output
    website_bucket_endpoint: Output
    certificate_arn: Optional[Output] = None
    price_class: CloudFrontDistributionPriceClassEnum = (
        CloudFrontDistributionPriceClassEnum.PriceClass_100
    )
    enabled: Optional[bool] = True
    wait_for_deployment: Optional[bool] = False
    cache_min_ttl: Optional[int] = 0
    cache_max_ttl: Optional[int] = 3600
    cache_default_ttl: Optional[int] = 600

    class Config:
        arbitrary_types_allowed = True
