import os
import json

from zendesk import ZendeskClient

def get_attribute_values():
    if os.path.exists("attributes.json"):
        return json.load(open("attributes.json"))

    zd = ZendeskClient()
    attribute_values = []

    attributes = zd.get('/routing/attributes.json')['attributes']
    attribute_values = []
    for attribute in attributes:
        attribute_values.extend(zd.get(f'/routing/attributes/{attribute["id"]}/values.json')['attribute_values'])
    json.dump(attribute_values, open("attributes.json","w+"))
    return attribute_values

def get_attribute_value_id(attribute_values, attribute_name):
    for attribute_value in attribute_values:
        conditions = attribute_value['conditions']['any']
        conditions.extend(attribute_value['conditions']['all'])
        for operator in conditions:
            if  operator['value'] == attribute_name:
                return {'id':attribute_value['id'],'name':attribute_value['name'], 'tag':attribute_name}
            