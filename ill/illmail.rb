#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require 'net/imap'
require 'kconv'
require "sqlite3"
require 'base64'
require 'nkf'
map.example.jp/g
imap = Net::IMAP.new('imap.example.jp')

imap.authenticate('PLAIN','username','password')
imap.examine('ILL')
imap.search(["TO","ILL"]).each do |message_id|
  #puts last_uid = imap.status('INBOX', ["MESSAGES"])["MESSAGES"]
  #puts message_id
  envelope = imap.fetch(message_id, "ENVELOPE")[0].attr["ENVELOPE"] 
  sender = envelope.sender[0].mailbox
  #body = imap.fetch(message_id, "BODY[TEXT]")[0].attr["BODY[TEXT]"].encode("UTF-8", "ISO-2022-JP")
  body = imap.fetch(message_id, "BODY[TEXT]")[0].attr["BODY[TEXT]"]
  body = NKF.nkf("-wmQ",body) #quoted-printableでデコードする
  date = envelope.date
  subject = envelope.subject
  subject = NKF.nkf("-w",subject)
#raise subject.encoding.to_s
  puts "#{message_id}"
  puts "送信者: #{sender}" 
  puts "送信日時#{date}"
  puts "件名: #{subject}"
  puts "本文:\n#{body} "
  db = SQLite3::Database.new("inbox.db")
  db.transaction{
  db.execute("INSERT OR IGNORE INTO mailbox values(?, ?, ?, ?, ?);", message_id, sender, date, subject, body)
  }
end
  #db = SQLite3::Database.new("test.db")
  #db.execute("select * from mailbox;"){|row| 
   # printf("----☆☆----\n送信者:%s\n送信日時:%s\n件名:%s\n本文:\n%s",row[1],row[2],row[3],row[4])}

