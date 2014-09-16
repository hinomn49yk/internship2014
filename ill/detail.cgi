#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require "cgi"
require "sqlite3"
require "library_stdnums"
print "Content-type: text/html\n\n"

print "<!DOCTYPE html>"
print "<html lang=\"ja\">"

cgi = CGI.new
illnum = cgi['illnum']

db = SQLite3::Database.new("ill.db")
db.transaction{
  rows = db.execute("select * from illrecord where illnum =\"#{illnum}\";") {|row| 
    print (<<-"HEAD")
    <head>
    <meta charset="utf-8">
    <title>#{row[10]}</title>
    <link rel="stylesheet" href="style.css">
    </head>\n
    HEAD
    
    puts "<body>"
    puts "<a href=\"illmanager.cgi\">受信トレイに戻る</a>"
 
    puts "<p><h2>#{row[10]}</h2></p><hr>"

    puts "<form action=\"status.cgi\" method=\"get\"><input type=\"text\" name=\"illstatus\" size=\"20\"><input type=\"hidden\" name=\"illnum\" value=\"#{row[0]}\"><input type=\"submit\" value=\"状態変更\"></form>"
    print '<form action="status.cgi" method="get"><select name="illstatus" ><option value="準備中" selected>準備中</option><option value="到着処理中">到着処理中</option><option value="済">済</option><option value="キャンセル">キャンセル</option><input type="submit" value="状態変更">'
    puts "<input type=\"hidden\" name=\"illnum\" value=\"#{row[0]}\"></form>"

    puts "<form action=\"status.cgi\" method=\"get\"><input type=\"text\" name=\"library\" size=\"20\"><input type=\"hidden\" name=\"illnum\" value=\"#{row[0]}\"><input type=\"submit\" value=\"図書館登録\"></form>"
    puts "<form action=\"status.cgi\" method=\"get\"><input type=\"text\" name=\"fees\" size=\"20\"><input type=\"hidden\" name=\"illnum\" value=\"#{row[0]}\"><input type=\"submit\" value=\"金額登録\"></form>"
    puts("<table><tr><td><br></td></tr>")
    db.execute("select * from illstatus where illnum = \"#{row[0]}\";"){| row |
      puts("<tr><td>ILL状態</td><td>#{row[1]}</td>")
      puts("<tr><td>変更日付</td><td>#{row[2]}</td>")
      puts("<tr><td>依頼した図書館</td><td>#{row[3]}</td>")
      puts("<tr><td>複写料金</td><td>#{row[4]}</td>")
      
    }

printf("<tr><td>通し番号</td><td>%s</td></tr>
<tr><td>受付日時</td><td>%s</td></tr>
<tr><td>[所属地区]</td><td>%s</td></tr>
<tr><td>[所属]</td><td>%s</td></tr>
<tr><td>[氏名]</td><td>%s</td></tr>
<tr><td>[内線番号]</td><td>%s</td></tr>
<tr><td>[E-mail]</td><td>%s</td></tr>
<tr><td>[引落し先 配算体コード]</td><td>%s</td></tr>
<tr><td>[予算科目コード（数字10桁）]</td><td>%s</td></tr>
<tr><td>[予算科目名称]</td><td>%s</td></tr>

<tr><td>[雑誌名/書籍名]</td><td>%s</td></tr>
<tr><td>[vol_no]</td><td>%s</td></tr>
<tr><td>[pages]</td><td>%s</td></tr>
<tr><td>[year]</td><td>%s</td></tr>
<tr><td>[author]</td><td>%s</td></tr>
<tr><td>[article]</td><td>%s</td></tr>
<tr><td>[ISSN]</td><td>%s</td></tr>
<tr><td>[ISBN]</td><td>%s</td></tr>
<tr><td>[note]</td><td>%s</td></tr></table><hr>",
 row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19])
  
  issn = row[16]
  isbn = row[17]
  if issn.empty? && isbn.empty?
    puts "ISBNとISSNがどちらも入力されていません"
  else
    if issn.empty?
      if StdNum::ISBN.valid?(isbn)
        puts "<p>#{isbn} has a valid checkdigit</p>"
        p cinii = "http://ci.nii.ac.jp/books/search?isbn=#{isbn}"
        p wc = "http://www.worldcat.org/search?q=bn:#{isbn}"
      else
        puts "<h2>ISBNが間違っています</h2>"
      end
    elsif isbn.empty?
      if StdNum::ISSN.valid?(issn)
        puts "<p>#{issn} has a valid checkdigit</p>"
        key = issn
        p cinii = "http://ci.nii.ac.jp/books/search?issn=#{issn}"
        p wc = "http://www.worldcat.org/search?q=n2:#{issn}"
      else
        puts "<h2>ISSNが間違っています</h2>" 
      end
    end
  end
  puts "<p><a href=\"#{cinii}\">CiNii Books</a></p>"
  puts "<p><a href=\"#{wc}\">WorldCat</a></p>"
  }
p rows
}
print "</body></html>"
