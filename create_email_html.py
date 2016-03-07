from parse_Gcalendar import *
from datetime import datetime, timedelta
import sys

# select one of the following:
IA_pole = 'IA'  # unified digest
# IA_pole = 'Porto'
# IA_pole = 'Lisbon'


# download the updated ICS file from the Google calendar
update_calendarICS()


def get_week_dates(today=None):
    if today is None:
        today = datetime.now()

    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=4)
    weekdates = start.strftime('%d/%b/%Y') + ' -- ' + end.strftime('%d/%b/%Y')
    return start, end, weekdates

start, end, weekdates = get_week_dates()
fileid = 'WeekDigest.' + start.strftime('%d%b%Y') + '.' + end.strftime('%d%b%Y') + '.html'

if IA_pole == 'IA':
    with open('email_template.html') as f:
        email_template = f.read()
elif IA_pole == 'Porto':
    with open('email_template_Porto.html') as f:
        email_template = f.read()
elif IA_pole == 'Lisbon':
    with open('email_template_Lisbon.html') as f:
        email_template = f.read()
else:
    print 'set IA_pole!'
    sys.exit(1)



google_calendar_link = 'http://www.google.com/calendar/render?action=TEMPLATE'
google_calendar_link+= '&text=%s'
google_calendar_link+= '&dates=%s/%s'
google_calendar_link+= '&details=%s'
google_calendar_link+= '&location=%s'
google_calendar_link+= '&sf=true&output=xml'


seminar_content = ''
iteration = 0

while True:
    datein = raw_input('Date of the seminar (DD-MM-YYYY) [empty to stop]: ')
    if datein == '':
        break

    if iteration == 0:
        date_of_week = datetime.strptime(datein, '%d-%m-%Y')
        start, end, weekdates = get_week_dates(today=date_of_week)
        fileid = 'WeekDigest.' + start.strftime('%d%b%Y') + '.' + end.strftime('%d%b%Y') + '.html'
        print fileid

    title, presenter, abstract, startime, dtstart, location, icslink = get_info_from_gcalendar(datein, IA_pole, type_of_event='S')
    link = ''

    seminar_content += '<h9><b>%s</b></h9> <br />\n' % title
    seminar_content += '<h9>%s</h9> <br />\n' % presenter
    seminar_content += '<p>%s</p>\n' % abstract
    seminar_content += '<br />\n'
    seminar_content += '<b><i>%s, %s</i></b>\n' % (location, startime)
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

progclub_content = ''
PC = raw_input('Is there a programmers club this week (y/[n]) ')
if PC == 'y':

    progclub = '\n<p class="lead">Also this week, there will be the Programmers Club:</p>\n'

    datein = raw_input('Date of the programmers club (DD-MM-YYYY): ')

    title, presenter, abstract, startime, dtstart, location, icslink = get_info_from_gcalendar(datein, IA_pole, type_of_event='PC')
    link = ''

    progclub_content += '<h9><b>%s</b></h9> <br />\n' % title
    progclub_content += '<h9>%s</h9> <br />\n' % presenter
    progclub_content += '<p>%s</p>\n' % abstract
    progclub_content += '<br />\n'
    progclub_content += '<b><i>%s, %s</i></b>\n' % (location, startime)
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


extra_content = ''
extra = raw_input('Anything else going on? (y/[n]) ')
if extra == 'y':

    extra_content += '<table>\n'
    extra_content += '<td><br>\n'
    extra_content += '  <p class="lead">In addition, the following events are also scheduled for this week.</p>\n'
    extra_content += '  <dl>\n'

    datein = raw_input('Date of the event (DD-MM-YYYY): ')

    title, presenter, abstract, startime, dtstart, location, icslink = get_info_from_gcalendar(datein, IA_pole, type_of_event='other')

    extra_event = ''
    extra_event += '      <dt><h9><b>%s</b></h9> <br></dt>\n' % title
    extra_event += '       <dd><h9>%s</h9> <br>\n' % presenter
    extra_event += '       <b><i>%s, %s</i></b>\n' % (location, startime)
    extra_event += '       <br />\n'

    datestart = time.strftime('%Y%m%dT%H%M00Z', dtstart)
    end = datetime(*dtstart[:6])+timedelta(hours=1)
    dateend = end.strftime('%Y%m%dT%H%M00Z')
    link = google_calendar_link % (title, datestart, dateend, presenter, location)
    # print link
    extra_event += 'Save this event to your calendar:\n'
    # progclub_content += '<a href="%s">Outlook</a> -- \n' % icslink
    # progclub_content += '<a href="%s">iCalendar</a> -- \n' % icslink
    extra_event += '<a href="%s">Google Calendar</a>\n' % link
    extra_event += '       </dd>\n'


    extra_content += extra_event
    extra_content += '  </dl>\n'
    extra_content += '  <hr style="background-color:#d9d9d9; border:none; color:#d9d9d9; height:1px" bgcolor="#d9d9d9" height="1">\n'
    extra_content += '  <hr style="background-color:#d9d9d9; border:none; color:#d9d9d9; height:1px" bgcolor="#d9d9d9" height="1">\n'
    extra_content += '</td>\n'
    extra_content += '</table>'

    email_template = email_template.replace('{{extrathings}}', extra_content)

else:
    email_template = email_template.replace('{{extrathings}}', '\n')



if (seminar_content=='' and progclub_content=='' and extra_content==''):
    print 
    print 'It seems there is nothing happening...'
    sys.exit(0)


# print repr(email_template)
email_template = unicode(email_template, 'utf8', 'replace')

# inline the CSS
from premailer import transform
email_template = transform(email_template)
print 'Successfully inlined CSS'


with open(fileid, 'w') as f:
    f.write(email_template.encode('utf8'))
    # f.write(email_template)

print 'Created the file %s' % fileid