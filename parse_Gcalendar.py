import urllib2
import os
import time
import re

icslink = ''

def update_calendarICS():
	global icslink
	calendarID = '2da6ql82pi4n8l4647026r5uvc%40group.calendar.google.com'
	
	icslink  = 'https://calendar.google.com/calendar/ical/'
	icslink += calendarID
	icslink += '/public/full/'
	# icslink += eventID
	# icslink += '.ics'
	icslink += 'basic.ics'
	

	# if not os.path.exists(eventID+'.ics'):
	response = urllib2.urlopen(icslink)
	content = response.read()
	with open('IAseminars.ics', 'w') as f:
		f.write(content)

	print 'Calendar file up to date'


def get_info_from_gcalendar(datein=None):
	global icslink
	if datein is None:
		datein = raw_input('Date of the seminar: (DD-MM-YYY) ')

	# ind = link.find('tmsrc=')
	# calendarID = link[ind+6:]
	# print 'cID = ', calendarID

	# link = link[:ind-1]

	# ind = link.find('tmeid=')
	# eventID = link[ind+6:]
	# print 'eID = ', eventID

	with open('IAseminars.ics') as f:
	    content = f.read()


	# split events
	individual_events = re.findall('BEGIN:VEVENT.*?END:VEVENT', content, flags=re.DOTALL)

	for event in individual_events:

		desc = re.findall('DESCRIPTION:.*?LAST-MODIFIED', event, flags=re.DOTALL)[0]
		desc = desc[12:-13]
		presenter = desc[:desc.find('\\n')]

		abstract = desc[desc.find('\\n'):]
		abstract = abstract.replace('\r\n ', '').replace('\\n', '').replace('\,', ',').replace('\;', ';')

		summary = re.findall('SUMMARY:.*?TRANSP', event, flags=re.DOTALL)[0]
		summary = summary[8:-6]
		# print repr(summary)
		summary = summary.replace('\r\n ', '').replace('\r\n', '').replace('\\n', '').replace('\,', ',')
		

		for line in event.split('\n'):
			line = line.strip()
			# print line

			if line.startswith('DTSTART:'):
				dtstart = line[8:].strip()
				dtstart = time.strptime(dtstart, '%Y%m%dT%H%M00Z')
				starttime = time.strftime('%d/%m/%Y, %H:%M', dtstart)
			
			# if line.startswith('DESCRIPTION:'): 
				# description = line
			if line.startswith('LOCATION:'):
				location = line[9:].strip()
			# if line.startswith('SUMMARY:'):
				# title = line[8:].strip()

		title = summary
		if time.strftime('%d-%m-%Y', dtstart) == datein:
			print 
			print summary
			print presenter
			print abstract
			break

	return title, presenter, abstract, starttime, dtstart, location, icslink