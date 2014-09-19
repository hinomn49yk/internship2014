#!/usr/bin/ruby
# -*- coding utf-8 -*-
require "open-uri"
require 'rexml/document'
require 'nokogiri'
require 'json'
require './illconfig'

def worldcatsearch(issn)
  oclc_uri = open("http://worldcat.org/issn/#{issn}", proxy: IllConfig.config["proxy_server"]).base_uri
  column = oclc_uri.path.split(/\//)
  oclcnum = column[-1]
  
  ur = "http://www.worldcat.org/oclc/" + "#{oclcnum}"
  uri = ur + ".rdf"
  doc = Nokogiri::XML(open(uri, proxy: IllConfig.config["proxy_server"]).read)
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
  result
end

p worldcatsearch("4101010056")
# uri.path = "/title/sorekara/oclc/25663089"

