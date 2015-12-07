from parse_Gcalendar import *
from datetime import datetime, timedelta
import sys

update_calendarICS()

today = datetime.now()
start = today - timedelta(days=today.weekday())
end = start + timedelta(days=4)
weekdates = start.strftime('%d/%b/%Y') + ' -- ' + end.strftime('%d/%b/%Y')
fileid = 'WeekDigest.' + start.strftime('%d%b%Y') + '.' + end.strftime('%d%b%Y') + '.html'




google_calendar_link = 'http://www.google.com/calendar/render?action=TEMPLATE'
google_calendar_link+= '&text=%s'
google_calendar_link+= '&dates=%s/%s'
google_calendar_link+= '&details=%s'
google_calendar_link+= '&location=%s'
google_calendar_link+= '&sf=true&output=xml'


seminar_content = ''

while True:
    datein = raw_input('Date of the seminar (DD-MM-YYYY) [empty to stop]: ')
    if datein == '':
        break

    title, presenter, abstract, startime, dtstart, location, icslink = get_info_from_gcalendar(datein)
    link = ''

    seminar_content += '<h9><b>%s</b></h9> <br />\n' % title
    seminar_content += '<h9>%s</h9> <br />\n' % presenter
    seminar_content += '<p>%s</p>\n' % abstract
    seminar_content += '<br />\n'
    seminar_content += '<i>%s, %s</i>\n' % (location, startime)
    seminar_content += '<br />\n'

    datestart = time.strftime('%Y%m%dT%H%M00Z', dtstart)
    end = datetime(*dtstart[:6])+timedelta(hours=1)
    dateend = end.strftime('%Y%m%dT%H%M00Z')

    link = google_calendar_link % (title, datestart, dateend, presenter, location)
    # print link

    seminar_content += 'Save this event to your calendar:\n'
    # seminar_content += '<a href="%s">Outlook</a> -- \n' % icslink
    # seminar_content += '<a href="%s">iCalendar</a> -- \n' % icslink
    seminar_content += '<a href="%s">Google Calendar</a>\n' % link

    seminar_content += '<hr />\n'
    seminar_content += '<hr />\n'
    seminar_content += '<br />\n'

    print '\n'

    iteration += 1


email_template = email_template.replace('{{seminars}}', seminar_content)
email_template = email_template.replace('{{weekdates}}', weekdates)

if IA_pole == 'Porto':
    progclub_content = ''
    PC = raw_input('Is there a programmers club this week (y/[n]) ')
    if PC == 'y':

        progclub = '\n<p class="lead">Also this week, there will be the Programmers Club:</p>\n'

        datein = raw_input('Date of the programmers club (DD-MM-YYYY): ')

        title, presenter, abstract, startime, dtstart, location, icslink = get_info_from_gcalendar(datein, IA_pole)
        link = ''

        progclub_content += '<h9><b>%s</b></h9> <br />\n' % title
        progclub_content += '<h9>%s</h9> <br />\n' % presenter
        progclub_content += '<p>%s</p>\n' % abstract
        progclub_content += '<br />\n'
        progclub_content += '<i>%s, %s</i>\n' % (location, startime)
        progclub_content += '<br />\n'

        datestart = time.strftime('%Y%m%dT%H%M00Z', dtstart)
        end = datetime(*dtstart[:6])+timedelta(hours=1)
        dateend = end.strftime('%Y%m%dT%H%M00Z')

        link = google_calendar_link % (title, datestart, dateend, presenter, location)
        # print link

        progclub_content += 'Save this event to your calendar:\n'
        # progclub_content += '<a href="%s">Outlook</a> -- \n' % icslink
        # progclub_content += '<a href="%s">iCalendar</a> -- \n' % icslink
        progclub_content += '<a href="%s">Google Calendar</a>\n' % link

        progclub_content += '<hr />\n'
        progclub_content += '<hr />\n'
        progclub_content += '<br />\n'
        print '\n'

        progclub_content = progclub + progclub_content
        email_template = email_template.replace('{{programmersclub}}', progclub_content)

    else:
        email_template = email_template.replace('{{programmersclub}}', '\n')

# print email_template

# inline the CSS
from premailer import transform
email_template = transform(email_template)



with open(fileid, 'w') as f:
    f.write(email_template)

print 'Created the file %s' % fileid