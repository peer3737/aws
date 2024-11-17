import boto3
from boto3.dynamodb.conditions import Attr
import json

def build_filter_expression(filters):
    filter_expression = None
# Dynamically build FilterExpression
    for attribute, condition in filters.items():
        for operator, value in condition.items():
            # Create condition based on operator
            if operator == 'eq':
                condition_expression = Attr(attribute).eq(value)
            elif operator == 'ne':
                condition_expression = Attr(attribute).ne(value)
            elif operator == 'lt':
                condition_expression = Attr(attribute).lt(value)
            elif operator == 'le':
                condition_expression = Attr(attribute).lte(value)
            elif operator == 'gt':
                condition_expression = Attr(attribute).gt(value)
            elif operator == 'ge':
                condition_expression = Attr(attribute).gte(value)
            elif operator == 'between':
                condition_expression = Attr(attribute).between(*value)
            elif operator == 'begins_with':
                condition_expression = Attr(attribute).begins_with(value)
            elif operator == 'in':
                # Create a chain of OR conditions for `in_`
                condition_expression = None
                for v in value:
                    if condition_expression is None:
                        condition_expression = Attr(attribute).eq(v)
                    else:
                        condition_expression |= Attr(attribute).eq(v)
            elif operator == 'contains':
                condition_expression = Attr(attribute).contains(value)
            elif operator == 'attribute_exists':
                condition_expression = Attr(attribute).exists()
            elif operator == 'attribute_not_exists':
                condition_expression = Attr(attribute).not_exists()
            else:
                raise ValueError(f"Unsupported operator: {operator}")

            # Combine conditions with AND (&)
            if filter_expression is None:
                filter_expression = condition_expression
            else:
                filter_expression &= condition_expression

    return filter_expression


def build_update_expression(update_data):
    """
    Build the UpdateExpression dynamically based on input data.
    """
    update_expression = "SET "
    expression_attribute_values = {}
    expression_attribute_names = {}

    for key, value in update_data.items():
        # Using ExpressionAttributeNames to avoid reserved words
        placeholder_key = f"#{key}"
        update_expression += f"{placeholder_key} = :{key}, "
        expression_attribute_values[f":{key}"] = value
        expression_attribute_names[placeholder_key] = key

    # Remove the trailing comma
    update_expression = update_expression.rstrip(', ')

    return update_expression, expression_attribute_values, expression_attribute_names


class Connection:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')


    def get(self, table_name, filters=None):
        table = self.dynamodb.Table(table_name)

        if filters is None:
            response = table.scan()
        else:

            # Query with the dynamically built FilterExpression
            response = table.scan(
                FilterExpression=build_filter_expression(filters)
            )

        # Print the results
        items = response['Items']
        return items


    def update(self, table_name, filters, update_data, primarykey='id'):
        table = self.dynamodb.Table(table_name)
    # Step 1: Build FilterExpression dynamically based on the filters

        # Step 2: Scan the table using the FilterExpression
        response = table.scan(FilterExpression=build_filter_expression(filters))
        items = response['Items']

        # Step 3: Build UpdateExpression dynamically based on the update data
        update_expression, expression_attribute_values, expression_attribute_names = build_update_expression(update_data)

        # Step 4: Update each item that matches the filter
        updated_items = {}

        for item in items:

            try:
                update = {}
                update_response = table.update_item(
                    Key={primarykey: item[primarykey]},  # Assuming 'primaryKey' is your primary key
                    UpdateExpression=update_expression,
                    ExpressionAttributeNames=expression_attribute_names,
                    ExpressionAttributeValues=expression_attribute_values,
                    ReturnValues="UPDATED_NEW"
                )
                for key_name, key_value in zip(expression_attribute_names.values(), expression_attribute_values.values()):
                    update[key_name] = key_value

                updated_items[item[primarykey]] = update


            except:
                continue

        return updated_items
