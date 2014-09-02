#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require "cgi"
require "sqlite3"
print "Content-type: text/html\n"
print "\n"
print "<!DOCTYPE html>"
print "<html lang=\"ja\">"
print "<head><meta charset=\"utf-8\"><title>削除</title></head>\n"
print "<body>"

# ASCIIであればうまくいく
cgi = CGI.new
 
isbn =  cgi["isbn"] 
title =  cgi["title"] 
author =  cgi["author"] 
pub = cgi["pub"] 
pubyear =cgi["pubyear"] 


db = SQLite3::Database.new("test.db")

db.transaction{
  db.execute("delete from bibrecord where isbn like ? or title like ? or author like ? or pub like ? or pubyear like ? ;", isbn, title, author, pub, pubyear)
  print "削除後のDB"
  print "<hr>"
  db.execute("select * from bibrecord;"){|row|
    print "<p>\n"
    printf("<h3>%s</h3> %s | %s<br> %s ISBN%s\n",row[1], row[2],row[3],row[4],row[0])

    print "</p>\n"
    print "<hr>"
  }

}

print "</body>\n"
print "</html>\n"
