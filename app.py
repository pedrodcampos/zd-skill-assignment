from zendesk import ZendeskClient

zd = ZendeskClient()

attributes = zd.get('/routing/attributes.json')['attributes']
attribute_values = []
for attribute in attributes:
    attribute_values.extend(zd.get(f'/routing/attributes/{attribute["id"]}/values.json')['attribute_values'])

a = 1
    