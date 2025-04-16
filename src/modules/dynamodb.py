from pulumi_aws.dynamodb import (
    Table,
    TableAttributeArgs,
)

from models.resources import DynamoDbTableCreateModel


class AmazonServiceDynamoDB:
    @staticmethod
    def set_attributes(attributes: list[dict[str, str]]) -> list[TableAttributeArgs]:
        result = []
        for attribute in attributes:
            for k, v in attribute.items():
                result.append(TableAttributeArgs(name=k, type=v))
        return result

    @staticmethod
    def create_table(table: DynamoDbTableCreateModel) -> Table:
        attributes = AmazonServiceDynamoDB.set_attributes(attributes=table.attributes)
        print(attributes)

        return Table(
            table.table_name,
            name=table.table_name,
            attributes=attributes,
            billing_mode=table.billing_mode,
            hash_key=table.hash_key,
            range_key=table.range_key,
            read_capacity=table.read_capacity,
            write_capacity=table.write_capacity,
        )
