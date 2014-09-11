#!/usr/bin/ruby
# -*- coding utf-8 -*-
require "open-uri"
require 'rexml/document'
require 'nokogiri'
require 'json'

issn = "00153230" 
#uri = open("http://worldcat.org/issn/13486780").base_uri
uri = open("http://worldcat.org/issn/09280987").base_uri
#uri = open("http://worldcat.org/isbn/4101010056").base_uri
# uri.path = "/title/sorekara/oclc/25663089"
column = uri.path.split(/\//)
oclcnum = column[-1]

#p uri = "http://www.worldcat.org/oclc/" + "#{oclcnum}" + ".jsonld"
ur = "http://www.worldcat.org/oclc/" + "#{oclcnum}"
#p uri = ur + ".nt" # nt
uri = ur + ".rdf"
doc = Nokogiri::XML(open(uri).read)
namespaces = {  
  "xmlns:rdf" => "http://www.w3.org/1999/02/22-rdf-syntax-ns#", 
  "xmlns:library" => "http://purl.org/library/",
  "xmlns:j.0" => "http://www.w3.org/2006/gen/ont#",
  "xmlns:owl" => "http://www.w3.org/2002/07/owl#",
  "xmlns:dcterms" => "http://purl.org/dc/terms/",
  "xmlns:xsd" => "http://www.w3.org/2001/XMLSchema#", 
  "xmlns:void" => "http://rdfs.org/ns/void#", 
  "xmlns:schema" => "http://schema.org/"
}

puts doc.xpath("//rdf:Description[@rdf:about='#{ur}']/schema:name", namespaces).text

#p uri = "http://www.worldcat.org/oclc/" + "#{oclcnum}" + ".jsonld"
=begin
<http://www.worldcat.org/oclc/25663089> <http://schema.org/name> "それから"
json = open(uri).read
test = JSON.parse(json)
=begin
require 'net/http'
proxy_class = Net::HTTP::Proxy('wwwout.nims.go.jp', 8888)
res = proxy_class.start('komorido.nims.go.jp'){| http |
  # proxy.example.com 経由で接続します。
  puts "a"
  p http
#  http.get('/~a013148/index.html/')
}
#puts res.body
#
#Net::HTTP.get_print 'http://worldcat.org', '/issn/13486780'

#doc = Nokogiri::HTML.parse(open("http://worldcat.org/isbn/4101010056"))
#doc = Nokogiri::HTML(open("http://worldcat.org/issn/13486780"))
#puts doc.title

#namespaces = {  
#  "xmlns" => "http://www.w3.org/2005/Atom", 
#  "xmlns:dc" => "http://purl.org/dc/elements/1.1/",
#  "xmlns:cinii" => "http://ci.nii.ac.jp/ns/1.0/",
#  "xmlns:dcterms" => "http://purl.org/dc/terms/" ,
#  "xmlns:opensearch" => "http://a9.com/-/spec/opensearch/1.1/" ,
#  "xmlns:prism" => "http://prismstandard.org/namespaces/basic/2.0/"
#}
#puts doc.xpath('//*').text
#puts "-----------------------------------------\n"


  puts doc.xpath("//xmlns:entry[#{i}]/xmlns:title", namespaces).text
  puts doc.xpath("//xmlns:entry[#{i}]/xmlns:author/xmlns:name", namespaces).text
  puts doc.xpath("//xmlns:entry[#{i}]/dc:publisher", namespaces).text
  puts doc.xpath("//xmlns:entry[#{i}]/prism:publicationDate", namespaces).text

=begin
doc = Nokogiri::XML(open("http://ci.nii.ac.jp/books/opensearch/search?isbn=4101010056"))
doc = Nokogiri::XML(open("http://ci.nii.ac.jp/books/opensearch/search?issn=13486780"))
=end
