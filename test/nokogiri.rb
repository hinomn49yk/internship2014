#!/usr/bin/ruby
# -*- coding utf-8 -*-
require "open-uri"
require 'rexml/document'
require 'nokogiri'

xml = <<EOM
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/" xmlns:prism="http://prismstandard.org/namespaces/basic/2.0/" xmlns:cinii="http://ci.nii.ac.jp/ns/1.0/" xmlns="http://www.w3.org/2005/Atom">
<title>CiNii Books OpenSearch - 4101010056</title>
<link href="http://ci.nii.ac.jp/books/search/?count=20&amp;sortorder=1&amp;isbn=4101010056&amp;advanced=true"/>
<link rel="self" type="application/atom+xml" href="http://ci.nii.ac.jp/books/opensearch/search?isbn=4101010056"/>
<id>http://ci.nii.ac.jp/books/opensearch/search?isbn=4101010056</id>
<updated>2014-09-08T09:19:10+0900</updated>
<opensearch:totalResults>3</opensearch:totalResults>
<opensearch:startIndex>0</opensearch:startIndex>
<opensearch:itemsPerPage>3</opensearch:itemsPerPage>
<entry>
<title>それから</title>
<link href="http://ci.nii.ac.jp/ncid/BA44499834"/>
<link rel="alternate" type="application/rdf+xml" href="http://ci.nii.ac.jp/ncid/BA44499834.rdf"/>
<id>http://ci.nii.ac.jp/ncid/BA44499834</id>
<author>
<name>夏目漱石著</name>
</author>
<dc:publisher>新潮社</dc:publisher>
<prism:publicationDate>1968</prism:publicationDate>
<updated>1968</updated>
<dcterms:isPartOf dc:title="新潮文庫">http://ci.nii.ac.jp/ncid/BN00424625</dcterms:isPartOf>
<dcterms:hasPart>urn:isbn:4101010056</dcterms:hasPart>
<cinii:ownerCount>9</cinii:ownerCount>
</entry>
<entry>
<title>それから</title>
<link href="http://ci.nii.ac.jp/ncid/BN11874011"/>
<link rel="alternate" type="application/rdf+xml" href="http://ci.nii.ac.jp/ncid/BN11874011.rdf"/>
<id>http://ci.nii.ac.jp/ncid/BN11874011</id>
<author>
<name>夏目漱石著</name>
</author>
<dc:publisher>新潮社</dc:publisher>
<prism:publicationDate>1985</prism:publicationDate>
<updated>1985</updated>
<dcterms:isPartOf dc:title="新潮文庫">http://ci.nii.ac.jp/ncid/BN00424625</dcterms:isPartOf>
<dcterms:hasPart>urn:isbn:4101010056</dcterms:hasPart>
<cinii:ownerCount>79</cinii:ownerCount>
</entry>
<entry>
<title>それから</title>
<link href="http://ci.nii.ac.jp/ncid/BB05057662"/>
<link rel="alternate" type="application/rdf+xml" href="http://ci.nii.ac.jp/ncid/BB05057662.rdf"/>
<id>http://ci.nii.ac.jp/ncid/BB05057662</id>
<author>
<name>夏目漱石著</name>
</author>
<dc:publisher>新潮社</dc:publisher>
<prism:publicationDate>2010</prism:publicationDate>
<updated>2010</updated>
<dcterms:isPartOf dc:title="新潮文庫">http://ci.nii.ac.jp/ncid/BN00424625</dcterms:isPartOf>
<dcterms:hasPart>urn:isbn:9784101010052</dcterms:hasPart>
<cinii:ownerCount>18</cinii:ownerCount>
</entry>
</feed>
EOM


#doc = Nokogiri::XML(xml)
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
#puts doc.xpath('//*').text
#puts "-----------------------------------------\n"

#puts doc.xpath('//cinii:ownerCount', "xmlns" => "http://www.w3.org/2005/Atom", "xmlns:dc" => "http://purl.org/dc/elements/1.1/", "xmlns:cinii" => "http://ci.nii.ac.jp/ns/1.0/").text
#puts doc.xpath('//xmlns:id', "xmlns" => "http://www.w3.org/2005/Atom", "xmlns:dc" => "http://purl.org/dc/elements/1.1/", "xmlns:cinii" => "http://ci.nii.ac.jp/ns/1.0/").text
i = 1
while i <= doc.xpath('//opensearch:totalResults', namespaces).text.to_i
  puts doc.xpath("//xmlns:entry[#{i}]/xmlns:title", namespaces).text
  puts doc.xpath("//xmlns:entry[#{i}]/xmlns:author/xmlns:name", namespaces).text
  puts doc.xpath("//xmlns:entry[#{i}]/dc:publisher", namespaces).text
  puts doc.xpath("//xmlns:entry[#{i}]/prism:publicationDate", namespaces).text
  puts "-----------------\n"
  i += 1
end
=begin
doc = Nokogiri::XML(open("http://ci.nii.ac.jp/books/opensearch/search?isbn=4101010056"))
doc = Nokogiri::XML(open("http://ci.nii.ac.jp/books/opensearch/search?issn=13486780"))
=end
