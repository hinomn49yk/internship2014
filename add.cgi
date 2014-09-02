#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require "cgi"
require "sqlite3"
require "isbn"
require "library_stdnums"
print "Content-type: text/html\n"
print "\n"
print "<!DOCTYPE html>"
print "<html lang=\"ja\">"
print "<head><meta charset=\"utf-8\"><title>追加</title></head>\n"
print "<body>"

cgi = CGI.new
isbn =  cgi["isbn"]
title =  cgi["title"] 
author =  cgi["author"] 
pub = cgi["pub"] 
pubyear = cgi["pubyear"] 
url = cgi["url"] 
issn = cgi["issn"] 

if isbn != "" && ISBN.valid?(isbn) != true 
  print "ISBNエラー</body></html>"
  exit(1)
end
if isbn != ""
  isbn = ISBN.thirteen(isbn)
end
if issn != "" && StdNum::ISSN.valid?(issn) != true
  print "ISSNエラー"
end

db = SQLite3::Database.new("test.db")

db.transaction{
  db.execute("insert into bibrecord VALUES(?, ?, ?, ?, ?, ?, ?)", isbn, title, author, pub, pubyear, url,issn)
  print "追加後のDB"
  print "<hr>"
  db.execute("select * from bibrecord;"){|row|
    print "<p>\n"
    printf("<h3>%s</h3> %s %s<br> %s ISBN%s\n",row[1], row[2],row[3],row[4],row[0])
    
    print "</p>\n"
    print "<hr>"
  }
  
}

print "</body>\n"
print "</html>\n"
