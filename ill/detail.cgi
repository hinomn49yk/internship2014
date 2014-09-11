#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require "cgi"
require "sqlite3"
require "library_stdnums"
print "Content-type: text/html\n\n"

print "<!DOCTYPE html>"
print "<html lang=\"ja\">"
print "<head><meta charset=\"utf-8\"></head>\n"
print"<a href=\"illmanager.cgi\">受信トレイに戻る</a>"
print "<body><h1>詳細</h1>\n"

cgi = CGI.new
p illnum = cgi['illnum']

db = SQLite3::Database.new("ill.db")
db.transaction{
rows = db.execute("select * from illrecord where illnum =\"#{illnum}\";") {|row| 
    printf("<table><tr><td><br></td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr>
<tr><td>%s</td></tr></table>", row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19])
  
  issn = row[16]
  isbn = row[17]
  if issn.empty? && isbn.empty?
    puts "ISBNとISSNがどちらも入力されていません"
  else
    if issn.empty?
      if StdNum::ISBN.valid?(isbn)
        puts "#{isbn} has a valid checkdigit"
      end
    elsif isbn.empty?
      if StdNum::ISSN.valid?(issn)
        puts "#{issn} has a valid checkdigit"
      end
    end
  end
  }
}
print "</body></html>"
