#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require 'cgi'
require 'nkf'
require 'sqlite3'
require 'library_stdnums'
print "Content-Disposition: attachment; filename=\"ill.csv\"\n"
print "Content-type: text/csv; charset=Shift_JIS\n\n"

cgi = CGI.new
illnum = cgi['illnum']
sql = cgi['sql']

db = SQLite3::Database.new("ill.db")
db.results_as_hash = true
if sql.empty? 
  sql = "
    SELECT illrecord.*, illstatus.fees
    FROM illrecord
    INNER JOIN illstatus
    ON illrecord.illnum = illstatus.illnum
    WHERE illrecord.illnum = \"#{illnum}\";"
end

db.execute(sql) {| row | 
  result = Hash[row.map{|key, value| [key, NKF.nkf('-s', value.to_s)]}]

  printf(
    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",
    result["site"],
    result["department"],
    result["name"],
    result["tell"],
    result["email"],
    result["code"],
    result["budget_code"],
    result["budget_name"],
    result["title"],
    result["fees"],
  )
}

