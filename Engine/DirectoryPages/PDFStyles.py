# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch


styles = getSampleStyleSheet()
# This is what sets Helvetica as the base font for the PrefixPages
styles.add(ParagraphStyle(name='PrefixBase',
                          fontName='Times-Roman',#Helvetica',
                          fontSize=14,
                          leading=1.3 * 14,
                          alignment=TA_CENTER))
# Here I create a style for the header pages
styles.add(ParagraphStyle(name='DocumentTitle',
                          parent=styles['PrefixBase'],
                          fontSize=30,
                          leading=1.2 * 30))
styles.add(ParagraphStyle(name='QuoteTitle',
                          parent=styles['PrefixBase'],
                          fontSize=26,
                          leading=1.2 * 26))
styles.add(ParagraphStyle(name='Subtitle',
                          parent=styles['PrefixBase'],
                          fontSize=18,
                          leading=1.2 * 18))
styles.add(ParagraphStyle(name='PrefixBaseRight',
                          parent=styles['PrefixBase'],
                          alignment=TA_RIGHT))
styles.add(ParagraphStyle(name='PrefixBaseLeft',
                          parent=styles['PrefixBase'],
                          alignment=TA_LEFT))
styles.add(ParagraphStyle(name='RegText',
                          fontsize=8,
                          alignment=TA_CENTER,
                          leading=1.5 * 8))
styles.add(ParagraphStyle(name='RegTextL',
                          parent=styles['RegText'],
                          alignment=TA_LEFT))
styles.add(ParagraphStyle(name='RegTextR',
                          parent=styles['RegText'],
                          alignment=TA_RIGHT))
styles.add(ParagraphStyle(name='DaveFooter',
                          parent=styles['Heading3'],
                          fontSize=8,
                          alignment=TA_CENTER))
styles.add(ParagraphStyle(name='DaveHeaderLeft',
                          parent=styles['Heading3'],
                          fontSize=8,
                          alignment=TA_LEFT))
styles.add(ParagraphStyle(name='DaveHeaderRight',
                          parent=styles['DaveHeaderLeft'],
                          alignment=TA_RIGHT))
styles.add(ParagraphStyle(name='DaveHeading',
                          parent=styles['Heading3'],
                          fontName='Times-Roman',
                          spaceAfter=0,
                          spaceBefore=0,
                          fontSize=8,
                          leading=1.5 * 8))
styles.add(ParagraphStyle(name='DaveBold',
                          parent=styles['DaveHeading'],
                          fontName='Times-Bold',
                          fontSize=10,
                          leading=1.5 * 10))
styles.add(ParagraphStyle(name='DaveBoldSmall',
                          parent=styles['DaveBold'],
                          fontSize = 8,
                          leading=1.5 * 8))
styles.add(ParagraphStyle(name='TextOnImage',
                          parent=styles['DaveBoldSmall'],
                          fontSize=7,
                          leading=1.2 * 7,
                          leftIndent=.06 * inch,
                          rightIndent=.06 * inch,
                          alignment=TA_CENTER))
