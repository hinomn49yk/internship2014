#!/usr/bin/ruby
# -*- coding utf-8 -*-

require "open-uri"
require 'rexml/document'


doc = REXML::Document.new(open("http://ci.nii.ac.jp/books/opensearch/search?isbn=4101010056"))
puts "-------------"
puts doc.elements['feed/entry/title'].text
puts doc.elements['feed/entry/author/name'].text
#puts doc.elements['feed/entry/dc:publisher'].text
# 名前空間があるためこれではエラーputs doc.elements['feed/entry/prism:publicationDate']
#doc.remove_namespaces!
#doc.elements['feed/entry/prism:publicationDate']

=begin
doc = REXML::Document.new(open("http://ci.nii.ac.jp/books/opensearch/search?issn=13486780"))
puts "-------------"
puts doc.elements['feed/entry/title'].text
puts doc.elements['feed/entry/author/name'].text
puts doc.elements['feed/entry/dc:publisher'].text
#puts doc.elements['feed/entry/prism:publicationDate']
=end
