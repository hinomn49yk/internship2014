#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require "sqlite3"
require "cgi"
require "isbn"
print "Content-type: text/html\n\n"

print "<!DOCTYPE html>"
print "<html lang=\"ja\">"
print "<head><meta charset=\"utf-8\"></head>\n"
print "<body><h1><a href=\"illbox.cgi\">ILL Manager</a></h1>\n"

print "<form action=\"search.cgi\" method=\"get\"><p><input type=\"search\" name=\"keyword\" size=\"50\"> 
<input type=\"submit\" value=\"検索\"></form>"


cgi = CGI.new
order = cgi["order"]

if order == "" 
  order = "desc"
end

print "<form action=\"illbox.cgi\" method=\"post\"><select name=\"order\">"
if order == "desc"
  print "<option value=\"desc\" selected>新しい順</option><option value=\"asc\">古い順</option>"
else
  print "<option value=\"desc\">新しい順</option><option value=\"asc\" selected>古い順</option>"
end
print "<input type=\"submit\" value=\"並び替え\"></form>"

db = SQLite3::Database.new("ill.db")
db.transaction{
  puts "<table border = 1>"
  puts "<tr><th>ILL状態</th><th>date</th><th>所属</th><th>氏名</th><th>Email</th><th>本・雑誌名</th></tr>"
  db.execute("select * from illrecord order by date #{order};"){| row | 
    printf("<tr><td>処理中</td><td>%s</td><td>%s, %s</td><td><form action=\"detail.cgi\" method=\"get\"><input type=\"hidden\" name=\"message_id\" value=\"%s\"><input type=\"submit\" value=\"%s\"></form></td><td>%s</td><td>%s</td></tr>",row[1], row[2], row[3], row[3], row[4], row[6],row[10])
  }
}
puts "</table>"
print "<p></p>\n"
print "</body></html>"
