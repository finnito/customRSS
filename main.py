#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import parsedatetime
from datetime import datetime
from pytz import timezone
import configparser

dt = datetime.now(timezone("Pacific/Auckland"))

calendar = parsedatetime.Calendar()

config = configparser.ConfigParser()
config.read('feeds.config')

index = open(f"public/index.html", "w")
index.truncate()
index.write(f"<!DOCTYPE HTML>\n\
<html lang='en'>\n\
<head>\n\
<meta charset=utf-8>\n\
<title>Custom Feeds Generated by Finn Le Sueur</title>\n\
</head>\n\
<body><p>I generate these feeds with a script because RNZ does not provide RSS feeds for tags.</p><ul>\n")

for section in config.sections():
	# Request website and parse
	r = requests.get(config[section]["url"])
	soup = BeautifulSoup(r.content, 'html.parser')

	# Select items from given container
	s = soup.select_one(config[section]["containerSelector"])
	items = s.select(config[section]["itemSelector"])

	f = open(f"public/{section}.xml", "w")
	f.truncate()
	f.write('<?xml version="1.0" encoding="utf-8" standalone="yes" ?>\n')
	f.write('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">\n')
	f.write('<channel>\n')
	f.write('<title>' + config[section]["title"] + '</title>\n')
	f.write('<link>' + config[section]['url'] + '</link>\n')
	f.write('<description>' + config[section]['url'] + '</description>\n')
	f.write('<atom:link href="https://feeds.lesueur.nz/' + section + '.xml" rel="self" type="application/rss+xml" />\n')
	f.write('<lastBuildDate>' + dt.strftime('%a, %d %b %Y %H:%M:%S %z') + '</lastBuildDate>\n')

	for item in items:
		# Extract files from each items.
		print(item)
		headline = item.select_one(config[section]["titleSelector"]).text.strip()
		summary = item.select_one(config[section]["descriptionSelector"]).text.strip()
		link = item.select_one(config[section]["linkSelector"]).get('href').strip()
		if not link.startswith("https"):
			link = config[section]["base"] + link
		datetime_object, status = calendar.parseDT(item.select_one(config[section]["dateSelector"]).text, tzinfo=timezone("Pacific/Auckland"))
		
		f.write('<item>\n')
		f.write('<title>' + headline + '</title>\n')
		f.write('<link>' + link + '</link>\n')
		f.write('<guid>' + link + '</guid>\n')
		f.write('<pubDate>' + datetime_object.strftime('%a, %d %b %Y %H:%M:%S %z') + '</pubDate>\n')
		f.write('<description>' + summary + '</description>\n')
		f.write('</item>\n')

	f.write('</channel>\n')
	f.write('</rss>')

	index.write(f"<li><a href='https://feeds.lesueur.nz/{section}.xml'>{config[section]['title']} > https://feeds.lesueur.nz/{section}.xml</a></li>\n")

index.write(f"</ul>\n<p>Find more information on <a href='https://github.com/finnito/customRSS'>GitHub</a></body>\n</html>")
