#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require 'cgi'
require 'nkf'
require 'sqlite3'
require 'library_stdnums'
print "Content-Disposition: attachment; filename=\"ill.txt\"\n"
print "Content-type: text/tsv; charset=Shift_JIS\n\n"

cgi = CGI.new
illnum = cgi['illnum']
query = cgi['query']

db = SQLite3::Database.new("ill.db")
db.results_as_hash = true
if query.empty? 
  if illnum.empty?
    sql = "
    SELECT illrecord.*, illstatus.fees
    FROM illrecord
    INNER JOIN illstatus
    ON illrecord.illnum = illstatus.illnum;

    "
  else 
    sql = "
    SELECT illrecord.*, illstatus.fees
    FROM illrecord
    INNER JOIN illstatus
    ON illrecord.illnum = illstatus.illnum
    WHERE illrecord.illnum = \"#{illnum}\";
    "
  end
else
  sql = "
    SELECT illrecord.*, illstatus.fees
    FROM illrecord
    INNER JOIN illstatus
    ON illrecord.illnum = illstatus.illnum
    WHERE illrecord.name like \"%#{query}%\";
  " 
end

print "site\tdepartment\tname\ttele\temail\tcode\tbudget_code\tbudget_name\ttitle\tfees\n"
db.execute(sql) {| row | 
  result = Hash[row.map{|key, value| [key, NKF.nkf('-s', value.to_s)]}]
  printf(
    "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n",
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

