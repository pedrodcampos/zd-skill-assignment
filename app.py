from zendesk import ZendeskClient
import csv
import attributes
import json
import time



def map_agent_skills():
    attribute_values = attributes.get_attribute_values()
    mapping = []
    with open('agent_product_mapping.csv') as f:
        rows = csv.reader(f)
        next(rows)
        for row in rows:
            mapping.append(
                {
                    "id":int(row[0]),
                    "name":row[1],
                    "email":row[2],
                    "skills":[attributes.get_attribute_value_id(attribute_values,skill) for skill in row[3].split(',')]
                }
            )
    json.dump(mapping, open("mapping.json","w+"))
    
def create_skills():
    map_agent_skills()
    mapping = json.load(open("mapping.json"))
    zd = ZendeskClient()
    errors=[]
    for agent in mapping:
        payload = {"attribute_value_ids":[skill['id'] for skill in agent['skills']]}
        result = zd.post(f'/routing/agents/{agent["id"]}/instance_values.json',json = payload)
        if result.status_code != 200:
            errors.append(agent)
        print(agent['name'],result)
    json.dump(errors, open("errors.json","w+"))
    
if __name__ == "__main__":
    create_skills()