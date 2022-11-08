from pulumi import Config

from modules.s3 import AmazonServiceS3
from modules.route53 import AmazonServiceRoute53
from modules.acm import AmazonServiceACM
from modules.cfn import AmazonServiceCfn
from modules.dynamodb import AmazonServiceDynamoDB
from models.resources import (
    DynamoDbTableCreateModel,
    Route53RecordCreateModel,
    CloudFrontDistributionCreateModel,
)

config = Config()
website_config = config.get_object("website")
route53_config = config.get_object("route53")
acm_config = config.get_object("acm")
cfn_config = config.get_object("cfn")

acm = AmazonServiceACM(domain=route53_config["domain"])
s3 = AmazonServiceS3()
route53 = AmazonServiceRoute53()
cfn = AmazonServiceCfn()
dynamodb = AmazonServiceDynamoDB()


# dynamodb table
dynamodb_table = DynamoDbTableCreateModel(
    table_name="scheduler", attributes=[{"days": "S"}, {"tasks": "L"}], hash_key="days"
)
dynamodb.create_table(table=dynamodb_table)


# static website & cloudfront bucket
website_bucket = s3.create_bucket(props=website_config)
cfn_bucket = s3.create_bucket(props=cfn_config)

# certificate for custom domain & cloudfront
certificate = acm.request_certificate(
    request_object="subdomain-certificate-object", domain_name=acm_config["domain"]
)
zone_id = route53.get_zone_id(name=route53_config["domain"])

cname_record = Route53RecordCreateModel(
    o="subdomain-cname-record",
    name=certificate.domain_validation_options.apply(
        lambda o: o[0].resource_record_name
    ),
    type="CNAME",
    records=[
        certificate.domain_validation_options.apply(
            lambda o: o[0].resource_record_value
        )
    ],
    zone_id=zone_id,
    ttl=600,
)
validation_record = route53.create_record(record=cname_record)
certificate_validation = acm.validate_certificate(
    validation_object="sudomain-validation-object",
    certificate_arn=certificate.arn,
    validation_record_fqdns=[validation_record.fqdn],
)

cfn_distribution = CloudFrontDistributionCreateModel(
    name="subdomain-cfn-distribution",
    aliases=[acm_config["domain"]],
    logging_bucket=cfn_bucket.bucket_domain_name,
    website_bucket_arn=website_bucket.arn,
    website_bucket_endpoint=website_bucket.website_endpoint,
    certificate_arn=certificate_validation.certificate_arn,
)
distribution = cfn.create_distribution(distribution=cfn_distribution)

# route53 alias for cloudfront distribution
a_record = Route53RecordCreateModel(
    o="subdomain-a-record",
    name=acm_config["domain"],
    type="A",
    aliases=[{distribution.domain_name: distribution.hosted_zone_id}],
    zone_id=zone_id,
)
route53.create_record(record=a_record)

# upload files to s3 bucket
s3.upload_to_bucket(bucket=website_bucket, path="../client/dist")
