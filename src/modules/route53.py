from pulumi_aws.route53 import Record, RecordAliasArgs, get_zone
from pulumi.output import Output

from models.resources import Route53RecordCreateModel


class AmazonServiceRoute53:
    @staticmethod
    def get_zone_id(name: str) -> str:
        zone_id = get_zone(name=name).id

        if not zone_id:
            raise ValueError(f"Zone ID for {name} not found.")

        return zone_id

    @staticmethod
    def set_attributes(
        aliases: list[dict[Output[str], Output[str]]] | None,
    ) -> list[RecordAliasArgs] | None:
        if not aliases:
            return None

        result = []
        for alias in aliases:
            for k, v in alias.items():
                result.append(
                    RecordAliasArgs(name=k, zone_id=v, evaluate_target_health=True)
                )
        return result

    @staticmethod
    def create_record(props: Route53RecordCreateModel) -> Record:
        aliases = AmazonServiceRoute53.set_attributes(aliases=props.aliases)

        return Record(
            resource_name=props.resource_name,
            name=props.name,
            type=props.type,
            records=props.records,
            aliases=aliases,
            zone_id=props.zone_id,
            ttl=props.ttl,
        )
