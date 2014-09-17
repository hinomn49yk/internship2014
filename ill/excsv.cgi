#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require "cgi"
require "nkf"
require "sqlite3"
require "library_stdnums"
print "Content-Disposition: attachment; filename='ill.csv'\n"
print "Content-type: text/csv; charset=Shift_JIS\n\n"

cgi = CGI.new
illnum = cgi['illnum']

db = SQLite3::Database.new("ill.db")
db.transaction{
  db.execute("select * from illrecord where illnum = \"#{illnum}\";") {|row| 
    #所属地区row[2]
    row.map!{|r| NKF.nkf('-s', r)}
    
    printf("%s,%s,%s,%s,%s,%s,%s,%s", row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
    
    db.execute("select * from illstatus where illnum = \"#{row[0]}\";"){| row |
    #  puts("#{row[4].encode("Shift_JIS")},") #複写料金row[4]
    }
  }
}
