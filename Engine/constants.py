# -*- coding: utf-8 -*-
from __future__ import unicode_literals



role_lst = ['bish', 'first', 'second', 'exec', 'clerk', 'fin', 'mem', "NULL",
            'hp', 'eq', 'rs', 'ym', 'yw', 'primary', 'ss', "NULL",
            'wml', 'news', 'miss']
role_dict = {'bish':	'Bishop',
             'first':	'1st Counselor',
             'second':	'2nd Counselor',
             'exec':	'Executive Secretary',
             'clerk':	'Ward Clerk',
             'fin':		'Financial Clerk',
             'mem':		'Membership Clerk',
             'hp':		'High Priest Group Leader',
             'eq':		'Elders Quorum President',
             'rs':		'Relief Society President',
             'ym':		"Young Men's President",
             'yw':		"Young Women's President",
             'primary':	'Primary President',
             'ss':		'Sunday School President',
             'wml':		'Ward Mission Leader',
             'news':	'Ward Newsletter',
             "NULL":	'',
             'miss':	'Missionaries'}


CONFIG_DEFAULTS = {
    "usequote": "1",
    "quotecontent": "As children of the Lord\nwe should strive every day to rise to a higher level of personal righteousness in all of our actions.",
    "quoteauthor": "President James E. Faust",

    "bldg_phone": "XXX-XXX-XXXX",
    "bldg_addy1": "Address Line 1",
    "bldg_addy2": "City, State ZIP CODE",

    'block_displaysac': '1',
    'block_sacstart': '09:00 AM', # 70 mins
    'block_displayss': '1',
    'block_ssstart': '10:20 AM', # 40 mins
    'block_display_pr_rs': '1',
    'block_pr_rs_start': '11:10 AM', # 50 mins

    'email_smtp': '',
    'email_username': '',
    'email_pass': '',
    'email_recipients': '',

    'file_images_directory': '',
    'file_image_archive_directory': '',
    'file_member_csv_location': '',
    'file_nonmember_csv_location': '',
    'file_dwellings_csv_location': '',
    'file_pdf_out_directory': '',

    'missing_missing_name': '',
    'missing_missingphone': '',
    'missing_overridephone': '0',

    'task_missreport': '1',
    'task_missimages': '1',
    'task_sendemail': '0',
    'task_genmissfile': '0',
    'task_extract_moveouts': '1',
    'task_genfull': '1',
    'task_genbooklet': '0',
    'task_gensingle2double': '0',

    'unit_unitname': 'Your Ward Name Here',
    'unit_unit_type': 'Ward',
    'unit_stakename': 'Your Stake Name Here',
}

for role in role_lst:
    if role == 'NULL':
        continue
    CONFIG_DEFAULTS['leadership_' + role + 'name'] = ''
    CONFIG_DEFAULTS['leadership_' + role + 'phone'] = ''
    CONFIG_DEFAULTS['leadership_' + role + 'overph'] = '0'
    CONFIG_DEFAULTS['leadership_' + role + 'disp'] = '1'
