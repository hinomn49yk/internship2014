#!/usr/bin/ruby
# -*- coding utf-8 -*-
require "open-uri"
require 'rexml/document'
require 'nokogiri'

#doc = Nokogiri::XML(xml)
#doc = Nokogiri::XML(open("http://ci.nii.ac.jp/books/opensearch/search?issn=13486780"))
#doc = Nokogiri::XML(open("http://ci.nii.ac.jp/books/opensearch/search?isbn=4101010056"))


def cinii_issn(issn)
  doc = Nokogiri::XML(open("http://ci.nii.ac.jp/books/opensearch/search?issn=#{issn}"))

  namespaces = {
    "xmlns" => "http://www.w3.org/2005/Atom", 
    "xmlns:dc" => "http://purl.org/dc/elements/1.1/",
    "xmlns:cinii" => "http://ci.nii.ac.jp/ns/1.0/",
    "xmlns:dcterms" => "http://purl.org/dc/terms/" ,
    "xmlns:opensearch" => "http://a9.com/-/spec/opensearch/1.1/" ,
    "xmlns:prism" => "http://prismstandard.org/namespaces/basic/2.0/"
  } 

  i = 1
  results = []
  while i <= doc.xpath('//opensearch:totalResults', namespaces).text.to_i
    result = {}
    result[:title]  = doc.xpath("//xmlns:entry[#{i}]/xmlns:title", namespaces).text
    result[:author] = doc.xpath("//xmlns:entry[#{i}]/xmlns:author/xmlns:name", namespaces).text
    result[:publisher] = doc.xpath("//xmlns:entry[#{i}]/dc:publisher", namespaces).text
    result[:pubdate] = puts doc.xpath("//xmlns:entry[#{i}]/prism:publicationDate", namespaces).text
    results << result
    i += 1
  end
  p results
end

def cinii_isbn(isbn)
  doc = Nokogiri::XML(open("http://ci.nii.ac.jp/books/opensearch/search?isbn=#{isbn}"))

  namespaces = {
    "xmlns" => "http://www.w3.org/2005/Atom", 
    "xmlns:dc" => "http://purl.org/dc/elements/1.1/",
    "xmlns:cinii" => "http://ci.nii.ac.jp/ns/1.0/",
    "xmlns:dcterms" => "http://purl.org/dc/terms/" ,
    "xmlns:opensearch" => "http://a9.com/-/spec/opensearch/1.1/" ,
    "xmlns:prism" => "http://prismstandard.org/namespaces/basic/2.0/"
  } 

  i = 1
  results = []
  while i <= doc.xpath('//opensearch:totalResults', namespaces).text.to_i
    result = {}
    result[:title]  = doc.xpath("//xmlns:entry[#{i}]/xmlns:title", namespaces).text
    result[:author] = doc.xpath("//xmlns:entry[#{i}]/xmlns:author/xmlns:name", namespaces).text
    result[:publisher] = doc.xpath("//xmlns:entry[#{i}]/dc:publisher", namespaces).text
    result[:pubdate] = puts doc.xpath("//xmlns:entry[#{i}]/prism:publicationDate", namespaces).text
    results << result
    i += 1
  end
  p results
end


#ciniisearch("0568-5230")



#puts doc.xpath('//*').text
#puts doc.xpath('//cinii:ownerCount', "xmlns" => "http://www.w3.org/2005/Atom", "xmlns:dc" => "http://purl.org/dc/elements/1.1/", "xmlns:cinii" => "http://ci.nii.ac.jp/ns/1.0/").text
