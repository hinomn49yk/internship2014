#!/usr/bin/ruby
# -*- coding utf-8 -*-
require "open-uri"
require 'rexml/document'
require 'nokogiri'

#doc = Nokogiri::XML(xml)
#doc = Nokogiri::XML(open("http://ci.nii.ac.jp/books/opensearch/search?issn=13486780"))
#doc = Nokogiri::XML(open("http://ci.nii.ac.jp/books/opensearch/search?isbn=4101010056"))


doc = Nokogiri::XML(open("http://ci.nii.ac.jp/books/opensearch/search?issn=13486780"))
namespaces = {
  "xmlns" => "http://www.w3.org/2005/Atom", 
  "xmlns:dc" => "http://purl.org/dc/elements/1.1/",
  "xmlns:cinii" => "http://ci.nii.ac.jp/ns/1.0/",
  "xmlns:dcterms" => "http://purl.org/dc/terms/" ,
  "xmlns:opensearch" => "http://a9.com/-/spec/opensearch/1.1/" ,
  "xmlns:prism" => "http://prismstandard.org/namespaces/basic/2.0/"
}

i = 1
while i <= doc.xpath('//opensearch:totalResults', namespaces).text.to_i
  puts doc.xpath("//xmlns:entry[#{i}]/xmlns:title", namespaces).text
  puts doc.xpath("//xmlns:entry[#{i}]/xmlns:author/xmlns:name", namespaces).text
  puts doc.xpath("//xmlns:entry[#{i}]/dc:publisher", namespaces).text
  puts doc.xpath("//xmlns:entry[#{i}]/prism:publicationDate", namespaces).text
  puts "-----------------\n"
  i += 1
end

#puts doc.xpath('//*').text
#puts doc.xpath('//cinii:ownerCount', "xmlns" => "http://www.w3.org/2005/Atom", "xmlns:dc" => "http://purl.org/dc/elements/1.1/", "xmlns:cinii" => "http://ci.nii.ac.jp/ns/1.0/").text
