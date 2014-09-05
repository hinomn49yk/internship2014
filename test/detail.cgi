#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require "cgi"
require "sqlite3"
require "isbn"
print "Content-type: text/html\n\n"

print "<!DOCTYPE html>"
print "<html lang=\"ja\">"
print "<head><meta charset=\"utf-8\"></head>\n"
print "<body><h1>詳細</h1>\n"

cgi = CGI.new
message_id = cgi['message_id']

db = SQLite3::Database.new("mail.db")
db.transaction{
  puts "<table border = 1>"
  puts "<tr><th>ILL状態</th><th>差出人:sender</th><th>送信日時:date</th><th>件名:subject</th><th>本文:body</th></tr>"
  db.execute("select * from mailbox where message_id =\"#{message_id.to_i}\";"){|row| 
    printf("<tr><td><br></td><td>%s</td><td>%s</td><td><a href=\"mailbox.cgi\">%s</a></td><td>%s</td></tr>",row[1],row[2],row[3],row[4])
  }
}
puts "</table>"

print "</body></html>"
