#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require 'sqlite3'
require 'cgi'
require 'library_stdnums'
print "Content-type: text/html\n\n"

print(<<"HEAD")
<!DOCTYPE html>
<html lang=\"ja\">
<head>
	<meta charset="utf-8">
	<title>ILL Manager</title>
	<link rel="stylesheet" href="style.css">
</head>
<body>
	<h1><a href=\"illmanager.cgi\">ILL Manager</a></h1>
HEAD


cgi = CGI.new
order = cgi["order"]
query = cgi["query"]

print(<<"SEARCH") 
	<form action=\"illmanager.cgi\" method=\"get\">
		<p><input type=\"search\" name=\"query\" size=\"50\" value=\"#{query}\">
		<input type=\"submit\" value=\"検索\"></p>
	</form>
SEARCH

if order.empty? ; order = "desc" end

puts "<form action=\"illmanager.cgi\" method=\"get\"><select name=\"order\">"
if order == "desc"
  puts "<option value=\"desc\" selected>新しい順</option><option value=\"asc\">古い順</option>"
else
  puts "<option value=\"desc\">新しい順</option><option value=\"asc\" selected>古い順</option>"
end
puts "</select><input type=\"submit\" value=\"並び替え\"><input type=\"hidden\" name=\"query\" value=\"#{query}\"></form>"


if query.empty?
  sql =  "SELECT illrecord.*, illstatus.status FROM illrecord INNER JOIN illstatus ON illrecord.illnum=illstatus.illnum WHERE illrecord.name like ? OR 1 = 1 ORDER BY date #{order}"
  #sql = "select * from illrecord where name like ? or 1 = 1 order by date #{order}"
else
  sql =  "SELECT illrecord.*, illstatus.status FROM illrecord INNER JOIN illstatus ON illrecord.illnum=illstatus.illnum WHERE illrecord.name like ? ORDER BY date #{order}"
end



db = SQLite3::Database.new("ill.db")
db.results_as_hash = true
db.transaction{
  puts "<table>"
  puts "<tr><th>ILL状態</th><th>通し番号</th><th>date</th><th>所属</th><th>氏名</th><th>Email</th><th>本・雑誌名</th><th>ISBN/ISSN</th></tr>"
  db.execute(sql, "%#{query}%") {| row | 
  #db.execute(sql) {| row | 
    printf(<<-RECORD, row['status'], row['illnum'], row['date'], row['site'], row['department'], row['name'], row['email'], row['title'], row['illnum'])
	<tr><td>%s</td><td>%s</td><td>%s</td><td>%s, %s</td><td>%s</td><td>%s</td>
	<td><form action="status.cgi" method="get">
	<input type=\"submit\" value=\"%s\"><input type=\"hidden\" name=\"illnum\" value=\"%s\">
	</form></td>
    RECORD

    issn = row['issn']
    isbn = row['isbn']
    if issn.empty? && isbn.empty?
      puts "\t<td>ISBNとISSNがどちらも入力されていません</td>"
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
          puts "<td><h2>#{issn}が間違っています<h2/></td>"
        end
      end
    end
    puts "</tr>"
  }
}
puts "</table>\n</body>\n</html>"
