#!/usr/bin/python
# -*- coding: MS932 -*-
import urllib
import urllib2
import cookielib


def _fetch_tickets(report_id, report_name, milestone, labo_value):
    filename = 'cookie.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    postdata = urllib.urlencode({
        'stuid': 'chen_xi',
        'pwd': 'chen_xi'
    })
    loginUrl = 'http://192.168.164.4/trac/cim/login'
    result = opener.open(loginUrl, postdata)
    cookie.save(ignore_discard=True, ignore_expires=True)


    url = 'http://narga/prm/report/custom/search'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    form_data = {
        'authenticityToken': '72c54e0a5f96e3b7353f2083b0909b46e2b32011',
        'docCustomReport.id': report_id,
        'docCustomReport.reportGroup': '1',
        'docCustomReport.name': report_name,
        'docCustomReport.queryMap.ticket_milestone.mode': '等しい',
        'docCustomReport.queryMap.ticket_milestone.values': milestone,
        'docCustomReport.queryMap.docs_labo.mode': '等しい',
        'docCustomReport.queryMap.docs_labo.values': labo_value,
        'docCustomReport.cols': 'docs_ticket_id',
        'docCustomReport.cols': 'ticket_summary',
        'docCustomReport.cols': 'docs_doc_dev',
        'docCustomReport.cols': 'docs_doc_eva',
        'docCustomReport.maxRows': 0
    }
    headers = {'User-Agent': user_agent}
    data = urllib.urlencode(form_data)
    request = urllib2.Request(url, data, headers)

    return urllib2.urlopen(request)


if __name__ == '__main__':
    response = _fetch_tickets('310', 'Connector Team', '2016-12-VerUP', '22')
    print response.read()
