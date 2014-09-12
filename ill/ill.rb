#!/usr/bin/ruby
# -*- coding: utf-8 -*-
# ILL依頼のメールを読み込み、抽出してDBに格納するプログラム
require 'net/imap'
require 'kconv'
require "sqlite3"
require 'base64'
require 'nkf'
require 'time'

imap = Net::IMAP.new('ahaya.nims.go.jp')

imap.authenticate('PLAIN','a013148','NIMS392!')
imap.examine('INBOX') #INBOX,ILL
imap.search(["TO","ILL"]).each do |message_id| 
  #puts last_uid = imap.status('INBOX', ["MESSAGES"])["MESSAGES"]
  #puts message_id
  envelope = imap.fetch(message_id, "ENVELOPE")[0].attr["ENVELOPE"] 
  sender = envelope.sender[0].mailbox
  #body = imap.fetch(message_id, "BODY[TEXT]")[0].attr["BODY[TEXT]"].encode("UTF-8", "ISO-2022-JP")
  body = imap.fetch(message_id, "BODY[TEXT]")[0].attr["BODY[TEXT]"]
  body = NKF.nkf("-wmQ",body) #quoted-printableでデコードする
  date = envelope.date #=> Wed, 03 Sep 2014 14:08:48 +0900
  date = Time.parse(date)     #=> 2014-09-11 09:02:09 +0900 
  year = date.year.to_s
  date = date.to_s
  subject = envelope.subject
  subject = NKF.nkf("-w",subject)
  subjects = subject.split()
  mailnum = subjects[-1]
#raise subject.encoding.to_s
  #"#{message_id}"
  #"送信者: #{sender}" 
  #"送信日時#{date}"
  #puts "件名: #{subject}"
  #"本文:\n#{body} "
  #mailnum = message_id.to_s
  profile = Array.new
  record = Hash.new("") #デフォルト値を設定しておく（あとでDBに格納するときのために））
  records = Array.new 
  body.each_line do |line|
    line.chomp!
    case line
    when /\[所属地区\](.*)/
      profile << $1
    when /\[所属\](.*)/
      profile << $1
    when /\[氏名\](.*)/
      profile << $1
    when /\[内線番号\](.*)/
      profile << $1
    when /\[E-mail\](.*)/
      profile << $1
    when /\[引落し先 配算体コード\](.*)/
      profile << $1
    when /\[予算科目コード（数字10桁）\](.*)/
      profile << $1
    when /\[予算科目名称\](.*)/
      profile << $1
    when /<(\d+)件目>/  
      $num = $1.to_i 
      #2件以上のとき
      if $num >= 2
        records[$num - 2] = record
        record = Hash.new("")
      end
    when /\[雑誌名\/書籍名\](.*)/
      record.store("title", $1) 
    when /\[vol_no\](.*)/
      record.store("vol_no", $1) 
    when /\[pages\](.*)/
      record.store("pages", $1) 
    when /\[year\](.*)/
      record.store("year", $1) 
    when /\[author\](.*)/
      record.store("author", $1) 
    when /\[article\](.*)/
      record.store("article", $1)
    when /\[ISSN\](.*)/
      record.store("issn", $1) 
    when /\[ISBN\](.*)/
      record.store("isbn", $1) 
    when /\[note\](.*)/
      record.store("note", $1) 
    end
  end 
  #1件のときはそのレコードを、2件以上のときの最後のレコードを配列に格納
  records[$num - 1] = record
 
  db = SQLite3::Database.new("ill.db")
  db.transaction{
    i = 0
    t = Time.now
    while i < $num
      illnum = mailnum + "-" + (i + 1).to_s + "-" + year
      db.execute "INSERT OR IGNORE INTO illrecord
        (illnum, date, site, department, name, tell, email, code, budget_code, budget_name,
         title, vol_no, pages, year, author,article, issn, isbn, note) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
        [illnum, date, profile[0], profile[1], profile[2], profile[3], profile[4], profile[5], profile[6], profile[7],
        records[i]["title"], records[i]["vol_no"], records[i]["pages"], records[i]["year"], records[i]["author"], records[i]["article"], records[i]["issn"], records[i]["isbn"], records[i]["note"]]

      db.execute "INSERT OR IGNORE INTO illstatus (illnum) VALUES(?);", [illnum]

      i += 1
    end
  } 

end


