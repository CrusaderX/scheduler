from pulumi_aws.route53 import Record, RecordAliasArgs, get_zone
from typing import Dict, Optional

from models.resources import Route53RecordCreateModel


class AmazonServiceRoute53:
    @staticmethod
    def get_zone_id(name: str) -> str:
        return get_zone(name=name).id

    @staticmethod
    def set_attributes(aliases: list[Dict[str, Optional[str]]]) -> RecordAliasArgs:
        for alias in aliases:
            for k, v in alias.items():
                return RecordAliasArgs(name=k, zone_id=v, evaluate_target_health=True)

    @staticmethod
    def create_record(record: Route53RecordCreateModel) -> Record:
        aliases = (
            [(AmazonServiceRoute53.set_attributes(aliases=record.aliases))]
            if record.aliases
            else None
        )

        return Record(
            record.o,
            name=record.name,
            type=record.type,
            records=record.records,
            aliases=aliases,
            zone_id=record.zone_id,
            ttl=record.ttl,
        )
