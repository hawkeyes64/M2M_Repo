__author__ = 'Lewis'

# We need a schema... :(

from sqlobject import *
from sqlobject.mysql import builder


conn = builder()(user='root', password='fed_uni_mysqluser2014',
                 host='localhost', db='fed_uni_mac_cloud')


#class PhoneNumber(SQLObject):
#    _connection = conn
#    number = StringCol(length=14, unique=True)
#    owner = StringCol(length=255)
#    lastCall = DateTimeCol(default=None)

#PhoneNumber.createTable(ifNotExists=True)
#PhoneNumber.dropTable(ifExists=True)

#call = PhoneNumber.select(PhoneNumber.q.number=='(415) 555-1212')
#print call
#print call[0].owner