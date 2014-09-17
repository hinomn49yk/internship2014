#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require "cgi"
require "sqlite3"
require "library_stdnums"
print "Content-type: text/html\n\n"


cgi = CGI.new
illnum = cgi['illnum']
illstatus = cgi['illstatus']
fees = cgi['fees']
library = cgi['library']
fanum = cgi['fanum']
db = SQLite3::Database.new("ill.db")
db.transaction{
  rows = db.execute("select * from illrecord where illnum = \"#{illnum}\";") {|row| 
    print (<<-"HEAD")
    <!DOCTYPE html>
    <html lang=\"ja\">
    <head>
    	<meta charset="utf-8">
    	<title>#{row[10]}</title>
    	<link rel="stylesheet" href="style.css">
    </head>\n
    HEAD
    
    print (<<-"FORM")
    <body>
    	<a href=\"illmanager.cgi\">受信トレイに戻る</a>
    	<p><h2>#{row[10]}</h2></p><hr>
    	<form action=\"status.cgi\" method=\"get\"><input type=\"text\" name=\"illstatus\" size=\"20\"><input type=\"hidden\" name=\"illnum\" value=\"#{row[0]}\"><input type=\"submit\" value=\"状態変更\"></form>
    	<form action="status.cgi" method="get"><select name="illstatus" ><option value="準備中" selected>準備中</option><option value="到着処理中">到着処理中</option><option value="済">済</option><option value="キャン セル">キャンセル</option><input type="submit" value="状態変更"><input type=\"hidden\" name=\"illnum\" value=\"#{row[0]}\"></form>
    	<form action=\"status.cgi\" method=\"get\"><input type=\"text\" name=\"library\" size=\"20\"><input type=\"hidden\" name=\"illnum\" value=\"#{row[0]}\"><input type=\"submit\" value=\"図書館登録\"></form>
    	<form action=\"status.cgi\" method=\"get\"><input type=\"text\" name=\"fees\" size=\"20\"><input type=\"hidden\" name=\"illnum\" value=\"#{row[0]}\"><input type=\"submit\" value=\"金額登録\"></form>
    FORM
    
    print '	<form action="status.cgi" method="get"><select name="fanum" >'
    db.execute("select * from falib;") {| fa |
      puts "\t\t<option value=\"#{fa[0]}\">#{fa[1]}</option>"
    }
    
    puts "\t<input type=\"hidden\" name=\"illnum\" value=\"#{row[0]}\">\n\t<input type=\"submit\" value=\"図書館登録\">\n\t</form>"

    t = Time.new
    if illstatus.empty?  
    else 
      db.execute "UPDATE illstatus SET status = \"#{illstatus}\" WHERE illnum = \"#{illnum}\""
      db.execute "UPDATE illstatus SET date = \"#{t.to_s}\" WHERE illnum = \"#{illnum}\"" 
    end
    
    if fees.empty?  ; else db.execute "UPDATE illstatus SET fees = \"#{fees}\" WHERE illnum = \"#{illnum}\"" end
    if library.empty?  ; else db.execute "UPDATE illstatus SET library = \"#{library}\" WHERE illnum = \"#{illnum}\"" end
    if fanum.empty?  ; else db.execute "UPDATE illstatus SET fanum = \"#{fanum}\" WHERE illnum = \"#{illnum}\"" end


    # CSVエクスポート
    puts "<form action=\"excsv.cgi\" method=\"get\"><input type=\"hidden\" name=\"illnum\" value=\"#{row[0]}\"><input type=\"submit\" value=\"CSV\"></form>"
    
    puts("<table><tr><td><br></td></tr>")
    db.execute("select * from illstatus where illnum = \"#{row[0]}\";"){| row |
      printf(<<-STATUS, row[1], row[2], row[4])
	<tr><td>ILL状態</td><td>%s</td>
	<tr><td>変更日付</td><td>%s</td>
	<tr><td>複写料金</td><td>%s</td>
      STATUS
    }
    db.execute("select * from falib where fanum = \"#{fanum}\";"){| row | 
      printf(<<-LIB, row[0], row[1])
	<tr><td>FA番号</td><td>%s</td>
	<tr><td>依頼した図書館</td><td>%s</td> 
      LIB
    }
    printf(<<-ILL,row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19])
	<tr><td>通し番号</td><td>%s</td></tr>
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
	<tr><td>[note]</td><td>%s</td></tr>
	</table><hr>",
    ILL
  

  issn = row[16].strip
  isbn = row[17].strip
  if issn.empty? && isbn.empty?
    puts "ISBNとISSNがどちらも入力されていません"
  else
    if issn.empty?
      if StdNum::ISBN.valid?(isbn)
        puts "<p>#{isbn} has a valid checkdigit</p>"
        p cinii = "http://ci.nii.ac.jp/books/search?isbn=#{isbn}"
        p wc = "http://www.worldcat.org/search?q=bn:#{isbn}"
        p ndl = "https://ndlopac.ndl.go.jp/F/?func=find-a&find_code=WTYP&request=&request_op=AND&find_code=ISBN&request=#{ndl}&request_op=AND&find_code=WTI&request=&request_op=AND&find_code=WAU&request=&request_op=AND&find_code=WPU&request=&request_op=AND&find_code=CALL&request=&request_op=AND&find_code=&request=&request_op=AND&find_code=&request=&request_op=AND&find_code=&request=&chk_bigram=on&adjacent=N&chk_all=on&chk_fmt_BK=on&chk_fmt_SE=on&chk_fmt_WZ=on&chk_fmt_EL=on&chk_fmt_WK=on&chk_fmt_HA=on&chk_fmt_MP=on&chk_fmt_MI=on&chk_fmt_AC=on&chk_fmt_ZK=on&chk_fmt_KT=on&filter_code_4=WSL&filter_request_4=&filter_code_2=WYR&filter_request_2=&filter_code_3=WYR&filter_request_3=&filter_code_1=WLNT&filter_request_1=&x=75&y=12"
        p iss = "http://iss.ndl.go.jp/api/openurl?any=#{isbn}"
      else
        puts "<h2>ISBNが間違っています</h2>"
      end
    elsif isbn.empty?
      if StdNum::ISSN.valid?(issn)
        puts "<p>#{issn} has a valid checkdigit</p>"
        key = issn
        p cinii = "http://ci.nii.ac.jp/books/search?issn=#{issn}"
        p wc = "http://www.worldcat.org/search?q=n2:#{issn}"
        p ndl = "https://ndlopac.ndl.go.jp/F/ILDAH8NLF7RV3YQIBBU8DLD32SQ5Q4JBKHT3VMFSD5G2HIFG3C-44349?func=find-a&find_code=WTYP&request=&request_op=AND&find_code=WRD&request=&request_op=AND&find_code=ISSN&request=#{issn}&request_op=AND&find_code=WAU&request=&request_op=AND&find_code=WPU&request=&request_op=AND&find_code=CALL&request=&request_op=AND&find_code=&request=&request_op=AND&find_code=&request=&request_op=AND&find_code=&request=&chk_bigram=on&adjacent=N&chk_all=on&chk_fmt_BK=on&chk_fmt_SE=on&chk_fmt_WZ=on&chk_fmt_EL=on&chk_fmt_WK=on&chk_fmt_HA=on&chk_fmt_MP=on&chk_fmt_MI=on&chk_fmt_AC=on&chk_fmt_ZK=on&chk_fmt_KT=on&filter_code_4=WSL&filter_request_4=&filter_code_2=WYR&filter_request_2=&filter_code_3=WYR&filter_request_3=&filter_code_1=WLNT&filter_request_1=&x=71&y=7"
        p iss = "http://iss.ndl.go.jp/api/openurl?any=#{issn}"
      else
        puts "<h2>ISSNが間違っています</h2>" 
      end
    end
  end
  puts "<p><a href=\"#{cinii}\">CiNii Books</a></p>"
  puts "<p><a href=\"#{wc}\">WorldCat</a></p>"
  puts "<p><a href=\"#{ndl}\">NDL-OPAC</p>"
  puts "<p><a href=\"#{iss}\">国立国会図書館サーチ</p>"
  }
p rows, "デバッグ用"
}
print "</body></html>"
