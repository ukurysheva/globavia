from flask_table import Table, Col


# Declare your table
class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')


# Get some objects
class Country(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description


items = [dict(name='Код страны', description='countryCode'),
         dict(name='Наименование страны', description='countryName'),
         dict(name='Материк страны', description='countryContinent'),
         dict(name='Часовой пояс', description='countryWiki')]

# Populate the table
table = ItemTable(items)
