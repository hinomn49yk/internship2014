#!/usr/bin/ruby
# -*- coding utf-8 -*-
require "open-uri"
require 'rexml/document'
require 'nokogiri'
require 'json'

def worldcat(issn)
  uri = open("http://worldcat.org/issn/#{issn}").base_uri
  #uri = open("http://worldcat.org/isbn/4101010056").base_uri
  # uri.path = "/title/sorekara/oclc/25663089"
  column = uri.path.split(/\//)
  oclcnum = column[-1]

  ur = "http://www.worldcat.org/oclc/" + "#{oclcnum}"
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

  result = doc.xpath("//rdf:Description[@rdf:about='#{ur}']/schema:name", namespaces).text
end


puts worldcatsearch("00153230")
