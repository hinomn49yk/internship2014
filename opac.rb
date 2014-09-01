#!/usr/bin/ruby
#-*- encoding: utf-8 -*-

require "sqlite3"

print "Hello OPAC\n"

db = SQLite3::Database.new("test.db")

keyword = gets.chomp!
keyword = "%" + keyword + "%"

db.transaction{
  db.execute("select * from opac where isbn like ? or title like ? or author like ? or pub like ? or pubyear like ? ;", keyword, keyword, keyword, keyword,keyword){|row|
    p row  
  }
}
