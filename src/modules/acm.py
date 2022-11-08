from pulumi import ResourceOptions
from pulumi_aws import Provider, config
from pulumi_aws.acm import Certificate, CertificateValidation
from typing import Optional

REGION_AVAILABILITY_ZONE = "us-east-1"

# TODO: pydantic


class AmazonServiceACM:
    def __init__(self, domain: str) -> None:
        self.provider = Provider(
            domain,
            profile=config.profile,
            region=REGION_AVAILABILITY_ZONE,
        )

    def request_certificate(
        self,
        request_object: str,
        domain_name: str,
        validation_method: Optional[str] = "DNS",
    ) -> Certificate:
        return Certificate(
            request_object,
            domain_name=domain_name,
            validation_method=validation_method,
            opts=ResourceOptions(provider=self.provider),
        )

    def validate_certificate(
        self,
        validation_object: str,
        certificate_arn: str,
        validation_record_fqdns: list[str],
    ) -> str:
        return CertificateValidation(
            validation_object,
            certificate_arn=certificate_arn,
            validation_record_fqdns=validation_record_fqdns,
            opts=ResourceOptions(provider=self.provider),
        )
