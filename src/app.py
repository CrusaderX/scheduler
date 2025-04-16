from typing import Tuple
from pulumi import Config
from pulumi_aws.s3 import Bucket, BucketWebsiteArgs
from pulumi_aws.acm import CertificateValidation
from pulumi_aws.cloudfront import Distribution

from modules.s3 import AmazonServiceS3
from modules.route53 import AmazonServiceRoute53
from modules.acm import AmazonServiceACM
from modules.cfn import AmazonServiceCfn
from models.resources import (
    Route53RecordCreateModel,
    CloudFrontDistributionCreateModel,
    Route53RecordTypeEnum,
    S3BucketCreateModel,
    CertificateCreateModel,
    CertificateValidateModel,
)

config = Config("scheduler")

website_config = config.require_object("website")
route53_config = config.require_object("route53")
acm_config = config.require_object("acm")
cfn_config = config.require_object("cfn")


def create_buckets(s3: AmazonServiceS3) -> Tuple[Bucket, Bucket]:
    """
    Creates website and CloudFront (cfn) buckets and uploads content.

    Returns:
        A tuple (website_bucket, cfn_bucket).
    """
    website_bucket_props = S3BucketCreateModel(
        **website_config,
        website=BucketWebsiteArgs(index_document="index.html", error_document=""),
    )
    cfn_bucket_props = S3BucketCreateModel(**cfn_config)

    website_bucket: Bucket = s3.create_bucket(website_bucket_props)
    cfn_bucket: Bucket = s3.create_bucket(cfn_bucket_props)

    s3.upload_to_bucket(
        parent=website_bucket, props=website_bucket_props, root="../client/dist"
    )
    return website_bucket, cfn_bucket


def setup_certificate(acm: AmazonServiceACM, route53: AmazonServiceRoute53) -> Tuple[CertificateValidation, str]:
    """
    Requests a certificate for the custom domain, creates the DNS validation record, 
    and validates the certificate.

    Returns:
        A tuple (certificate_validation, zone_id).
    """
    certificate_props = CertificateCreateModel(
        resource_name="subdomain-certificate",
        domain_name=acm_config.get("domain"),
    )
    certificate = acm.request_certificate(props=certificate_props)

    zone_id: str = route53.get_zone_id(name=route53_config.get("domain"))

    cname_record_props = Route53RecordCreateModel(
        resource_name="subdomain-cname-record",
        name=certificate.domain_validation_options.apply(
            lambda o: o[0].resource_record_name or ""
        ),
        type=Route53RecordTypeEnum.CNAME,
        records=[
            certificate.domain_validation_options.apply(
                lambda o: o[0].resource_record_value or ""
            )
        ],
        zone_id=zone_id,
        ttl=600,
    )
    validation_record = route53.create_record(props=cname_record_props)

    certificate_validation_props = CertificateValidateModel(
        resource_name="subdomain-validation-certificate",
        certificate_arn=certificate.arn,
        validation_record_fqdns=[validation_record.fqdn],
    )
    certificate_validation = acm.validate_certificate(
        props=certificate_validation_props
    )
    return certificate_validation, zone_id


def create_distribution(
    cfn: AmazonServiceCfn,
    certificate_validation: CertificateValidation,
    website_bucket: Bucket,
    cfn_bucket: Bucket
) -> Distribution:
    """
    Creates a CloudFront distribution using the validated certificate and the buckets.

    Returns:
        The CloudFront distribution resource.
    """
    cfn_distribution_props = CloudFrontDistributionCreateModel(
        resource_name="subdomain-cfn-distribution",
        aliases=[acm_config.get("domain")],
        logging_bucket=cfn_bucket.bucket_domain_name,
        website_bucket_arn=website_bucket.arn,
        website_bucket_endpoint=website_bucket.website_endpoint,
        certificate_arn=certificate_validation.certificate_arn,
    )
    distribution = cfn.create_distribution(props=cfn_distribution_props)

    return distribution


def create_dns_records(route53: AmazonServiceRoute53, zone_id: str, distribution: Distribution) -> None:
    """
    Creates DNS records to point the custom domain to the CloudFront distribution.
    """
    a_record_props = Route53RecordCreateModel(
        resource_name="subdomain-a-record",
        name=acm_config.get("domain"),
        type=Route53RecordTypeEnum.A,
        aliases=[{distribution.domain_name: distribution.hosted_zone_id}],
        zone_id=zone_id,
    )
    route53.create_record(props=a_record_props)


if __name__ == "__main__":
    acm = AmazonServiceACM(resource_name=route53_config.get("domain"))
    s3 = AmazonServiceS3()
    route53 = AmazonServiceRoute53()
    cfn = AmazonServiceCfn()

    website_bucket, cfn_bucket = create_buckets(s3)
    certificate_validation, zone_id = setup_certificate(acm, route53)
    distribution = create_distribution(cfn, certificate_validation, website_bucket, cfn_bucket)

    create_dns_records(route53, zone_id, distribution)

