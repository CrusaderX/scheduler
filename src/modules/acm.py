from pulumi import ResourceOptions
from pulumi_aws import Provider, config
from pulumi_aws.acm import Certificate, CertificateValidation

from models.resources import CertificateCreateModel, CertificateValidateModel

REGION_AVAILABILITY_ZONE = "us-east-1"


class AmazonServiceACM:
    def __init__(self, resource_name: str) -> None:
        self.provider = Provider(
            resource_name=resource_name,
            profile=config.profile,
            region=REGION_AVAILABILITY_ZONE,
        )

    def request_certificate(self, props: CertificateCreateModel) -> Certificate:
        default = ResourceOptions(provider=self.provider)
        opts = ResourceOptions.merge(default, props.opts or ResourceOptions())

        return Certificate(
            resource_name=props.resource_name,
            domain_name=props.domain_name,
            validation_method=props.validation_method,
            opts=opts,
        )

    def validate_certificate(
        self, props: CertificateValidateModel
    ) -> CertificateValidation:
        default = ResourceOptions(provider=self.provider)
        opts = ResourceOptions.merge(default, props.opts or ResourceOptions())

        return CertificateValidation(
            resource_name=props.resource_name,
            certificate_arn=props.certificate_arn,
            validation_record_fqdns=props.validation_record_fqdns,
            opts=opts,
        )
