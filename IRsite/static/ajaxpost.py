#!/usr/bin/python
import sys
import json
import cgi, cgitb
from sys import argv



cgitb.enable()  # for troubleshooting

#the cgi library gets vars from html
data = cgi.FieldStorage()
# #this is the actual output
# print "Content-Type: text/html\n"
# print "The foo data is: " + data["foo"].value
# print "<br />"
# print "The bar data is: " + data["bar"].value
# print "<br />"
# print data


