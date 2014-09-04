#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require "cgi"
require "sqlite3"
require "isbn"
print "Content-type: text/html\n\n"

print "<!DOCTYPE html>"
print "<html lang=\"ja\">"
print "<head><meta charset=\"utf-8\"></head>\n"
print "<body><h1>受信トレイ</h1>\n"

db = SQLite3::Database.new("mail.db")
db.transaction{
  puts "<table border = 1>"
  puts "<tr><th>差出人:sender</th><th>送信日時:date</th><th>件名:subject</th><th>本文:body</th></tr>"
  db.execute("select * from mailbox;"){|row| 
    printf("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>",row[1],row[2],row[3],row[4])
  }
}
puts "</table>"
print "<p></p>\n"
print "</body></html>"
