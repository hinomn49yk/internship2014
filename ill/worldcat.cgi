#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require "sqlite3"
require "cgi"
require "isbn"
require "./worldcat"
print "Content-type: text/html\n\n"

cgi = CGI.new
print "<!DOCTYPE html>"
print "<html lang=\"ja\">"
print "<head><meta charset=\"utf-8\"></head>\n"
print "<body><h1>Worldcatの検索結果</h1>\n"
issn = cgi["issn"]
#issn = "03600564"
  puts "<div id = \"content\">"
  puts "<table><tr><th>WorldCat 検索結果</th></tr><tr><td>"
  puts worldcatsearch(issn)
  puts "</td></tr></div>"

print "</body></html>"
