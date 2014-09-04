#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require 'net/imap'
require 'kconv'
require "sqlite3"
require 'base64'
require 'nkf'
imap = Net::IMAP.new('ahaya.nims.go.jp')

imap.authenticate('PLAIN','a013148','NIMS392!')
imap.examine('INBOX')
imap.search(["TO","SEKINE"]).each do |message_id|
  #puts last_uid = imap.status('INBOX', ["MESSAGES"])["MESSAGES"]
  puts message_id
  envelope = imap.fetch(message_id, "ENVELOPE")[0].attr["ENVELOPE"] 
  body = imap.fetch(message_id, "BODY[TEXT]")[0].attr["BODY[TEXT]"].encode("UTF-8", "ISO-2022-JP")
  sender = envelope.sender[0].mailbox
  date = envelope.date
  subject = envelope.subject
  puts NKF.nkf("-w",subject)
#raise subject.encoding.to_s
  # "送信者: #{sender}" 
  #puts "送信#{date}"
  #puts "件名: #{subject}"
  #puts "本文:\n#{body} "
  #db = SQLite3::Database.new("mail.db")
  #db.transaction{
   # db.execute("insert into mailbox values(?, ?, ?, ?, ?);", message_id, sender, date, subject, body)
  #}
end
  #db = SQLite3::Database.new("test.db")
  #db.execute("select * from mailbox;"){|row| 
   # printf("----☆☆----\n送信者:%s\n送信日時:%s\n件名:%s\n本文:\n%s",row[1],row[2],row[3],row[4])}

