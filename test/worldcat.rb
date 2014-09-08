#!/usr/bin/ruby
# -*- coding utf-8 -*-
require "open-uri"
require 'rexml/document'
require 'nokogiri'
url = "http://worldcat.org/isbn/4101010056"

#doc = Nokogiri::HTML(open("http://worldcat.org/issn/13486780"))

doc = Nokogiri::HTML.parse(open("http://worldcat.org/isbn/4101010056"))
puts doc.title
doc.xpath('//div[]').each do |node|
  p node.xpath('//div').text  
end

=begin
<div id="bibdata">

	<h1 class="title"><div class=vernacular lang="ja">それから /</div>
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
