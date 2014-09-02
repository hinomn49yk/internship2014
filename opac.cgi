#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require "cgi"
require "sqlite3"
require "isbn"
print "Content-type: text/html\n"
print "\n"
print "<!DOCTYPE html>"
print "<html lang=\"ja\">"
print "<head><meta charset=\"utf-8\"></head>\n"
print "<body><h1>検索結果</h1>\n"
print "<p>Hello OPAC</p>\n"

cgi = CGI.new
keyword = cgi["keyword"]
print "keyword = #{keyword}"
keyword = "%" + keyword + "%"


print "<hr>"
db = SQLite3::Database.new("test.db")

db.transaction{
  db.execute("select * from bibrecord where isbn like ? or title like ? or author like ? or pub like ? or pubyear like ? ;", keyword, keyword, keyword, keyword,keyword){|row|
    print "<p>\n"
    printf("<h3>%s</h3> %s | %s<br> %s ISBN%s\n",row[1], row[2],row[3],row[4],row[0])
    
    print "</p>\n"
    print "<hr>"
  }
}

print "</body></html>"
