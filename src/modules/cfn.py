from pulumi_aws.cloudfront import (
    Distribution,
    DistributionOriginArgs,
    DistributionOriginCustomOriginConfigArgs,
    DistributionDefaultCacheBehaviorArgs,
    DistributionDefaultCacheBehaviorForwardedValuesArgs,
    DistributionDefaultCacheBehaviorForwardedValuesCookiesArgs,
    DistributionCustomErrorResponseArgs,
    DistributionViewerCertificateArgs,
    DistributionRestrictionsArgs,
    DistributionRestrictionsGeoRestrictionArgs,
    DistributionLoggingConfigArgs,
)

from models.resources import CloudFrontDistributionCreateModel


class AmazonServiceCfn:
    @staticmethod
    def create_distribution(
        distribution: CloudFrontDistributionCreateModel,
    ) -> Distribution:
        return Distribution(
            distribution.name,
            enabled=distribution.enabled,
            aliases=distribution.aliases,
            origins=[
                DistributionOriginArgs(
                    origin_id=distribution.website_bucket_arn,
                    domain_name=distribution.website_bucket_endpoint,
                    custom_origin_config=DistributionOriginCustomOriginConfigArgs(
                        origin_protocol_policy="http-only",
                        http_port=80,
                        https_port=443,
                        origin_ssl_protocols=["TLSv1.2"],
                    ),
                )
            ],
            default_root_object="index.html",
            default_cache_behavior=DistributionDefaultCacheBehaviorArgs(
                target_origin_id=distribution.website_bucket_arn,
                viewer_protocol_policy="redirect-to-https",
                allowed_methods=["GET", "HEAD", "OPTIONS"],
                cached_methods=["GET", "HEAD", "OPTIONS"],
                forwarded_values=DistributionDefaultCacheBehaviorForwardedValuesArgs(
                    cookies=DistributionDefaultCacheBehaviorForwardedValuesCookiesArgs(
                        forward="none"
                    ),
                    query_string=False,
                ),
                min_ttl=distribution.cache_min_ttl,
                default_ttl=distribution.cache_default_ttl,
                max_ttl=distribution.cache_max_ttl,
            ),
            price_class=distribution.price_class,
            custom_error_responses=[
                DistributionCustomErrorResponseArgs(
                    error_code=404, response_code=404, response_page_path="/404.html"
                )
            ],
            viewer_certificate=DistributionViewerCertificateArgs(
                acm_certificate_arn=distribution.certificate_arn,
                ssl_support_method="sni-only",
            ),
            restrictions=DistributionRestrictionsArgs(
                geo_restriction=DistributionRestrictionsGeoRestrictionArgs(
                    restriction_type="none"
                )
            ),
            logging_config=DistributionLoggingConfigArgs(
                bucket=distribution.logging_bucket,
                include_cookies=False,
            )
            if distribution.logging_bucket
            else None,
            wait_for_deployment=distribution.wait_for_deployment,
        )
