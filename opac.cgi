#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require "cgi"
require "sqlite3"


print "Content-type: text/html\n"
print "\n"
print "<html>"
print "<head><meta charset=\"utf-8\"> </head>"
print "<body><h1>検索結果</h1>"
print "<p>Hello OPAC</p>"

db = SQLite3::Database.new("test.db")

cgi = CGI.new
keyword = cgi["keyword"]
print "#{keyword}"
#keyword = gets.chomp!
keyword = "%" + keyword + "%"

db.transaction{
  db.execute("select * from opac where isbn like ? or title like ? or author like ? or pub like ? or pubyear like ? ;", keyword, keyword, keyword, keyword,keyword){|row|
    p row
  }
}

print "</body></html>"
