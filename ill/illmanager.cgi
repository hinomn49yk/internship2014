#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require "sqlite3"
require "cgi"
require 'library_stdnums'
print "Content-type: text/html\n\n"

print (<<"HEAD")
<!DOCTYPE html>
<html lang=\"ja\">
<head>
	<meta charset="utf-8">
	<title>ILL Manager</title>
	<link rel="stylesheet" href="style.css">
</head>\n
HEAD

puts "<body><h1><a href=\"illmanager.cgi\">ILL Manager</a></h1>"


cgi = CGI.new
order = cgi["order"]
query = cgi["query"]
puts "<form action=\"illmanager.cgi\" method=\"get\"><p><input type=\"search\" name=\"query\" size=\"50\" value=\"#{query}\"><input type=\"submit\" value=\"検索\"></form>"

if order == "" 
  order = "desc"
end
print "<form action=\"illmanager.cgi\" method=\"post\"><select name=\"order\">"
if order == "desc"
  print "<option value=\"desc\" selected>新しい順</option><option value=\"asc\">古い順</option>"
else
  print "<option value=\"desc\">新しい順</option><option value=\"asc\" selected>古い順</option>"
end
puts "<input type=\"submit\" value=\"並び替え\"></form>"




if query.empty?
  sql = "select * from illrecord order by date #{order};"
else
  sql = "select * from illrecord where name like \"%#{query}%\"order by date #{order};"
end


db = SQLite3::Database.new("ill.db")
db.transaction{
  puts "<table><tr><th>ILL状態</th><th>通し番号</th><th>date</th><th>所属</th><th>氏名</th><th>Email</th><th>本・雑誌名</th><th>ISBN/ISSN</th></tr>"
  db.execute(sql) {| row | 
    # ILL状態を表示
    db.execute("select status from illstatus where illnum = \"#{row[0]}\";"){| row | 
      puts("<tr><td>#{row[0]}</td>")
    }
    # 依頼情報を表示
    printf("<td>%s</td><td>%s</td><td>%s, %s</td><td>%s</td><td>%s</td>
<td><form action=\"status.cgi\" method=\"get\"><input type=\"submit\" value=\"%s\"><input type=\"hidden\" name=\"illnum\" value=\"%s\"></form></td>",
row[0], row[1], row[2], row[3], row[4], row[6], row[10], row[0])
  issn = row[16]
  isbn = row[17]
  if issn.empty? && isbn.empty?
    puts "<td>ISBNとISSNがどちらも入力されていません</td>"
  else
    if issn.empty?
      if StdNum::ISBN.valid?(isbn)
        puts "<td>#{isbn} has a valid checkdigit</td>"
      else
        puts "<td><h2>#{isbn}が間違っています<h2/></td>"
      end
    elsif isbn.empty?
      if StdNum::ISSN.valid?(issn)
        puts "<td>#{issn} has a valid checkdigit</td>"
      else
        puts "<td><h2>#{isbn}が間違っています<h2/></td>"
      end
    end
  end
  print "</tr>"
  }
}
puts "</table>"
print "</body></html>"
