# -*- coding: utf-8 -*-
import sys
import logging
from lxml import etree
from sabreclient import SabreClient, SabreClientException
from settings import sabre as sabre_settings

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


def segments(record_locator):
    """Returns number of segments in a given PNR"""
    client = SabreClient(sabre_settings['pos'])
    try:
        pnr = client.pnr(record_locator)
        ns = pnr.nsmap
        if None in ns:
            ns['xmlns'] = ns[None]
            ns.pop(None)
        segments = pnr.findall('.//xmlns:ReservationItems//xmlns:FlightSegment', namespaces=ns)
        travelers = pnr.findall('.//xmlns:CustomerInfo/xmlns:PersonName', namespaces=ns)
    except SabreClientException:
        print client.request_text
        print client.response_text
        raise
    return pnr

if __name__ == '__main__':
    from lxml import etree
    pnr = 'YFCDVY'
    r = segments(pnr)
    #print etree.tostring(r)
