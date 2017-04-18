# -*- coding: utf-8 -*-
import sys
import logging
from lxml import etree
from sabreclient import SabreClient, SabreClientException
from settings import sabre as sabre_settings

log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


def calc_bookings(pnr_record_locator):
    """Returns number of bookings in a given PNR.

    Number of bookings (sold segments) is multiplication of
    number of itinerary segments and number of travelers.
    This function doesn't check tickets information, segments statuses, etc.
    """
    bookings = 0
    client = SabreClient(sabre_settings['pos'])
    try:
        pnr = client.pnr(pnr_record_locator)
        ns = pnr.nsmap
        if None in ns:
            ns['xmlns'] = ns[None]
            ns.pop(None)
        segments = pnr.findall('.//xmlns:ReservationItems//xmlns:FlightSegment', namespaces=ns)
        travelers = pnr.findall('.//xmlns:CustomerInfo/xmlns:PersonName', namespaces=ns)
        bookings = len(segments)*len(travelers)
    except SabreClientException:
        log.error('Cannot calculate bookings in PNR %s' % pnr_record_locator)
        log.debug('Calculator PNR %s, broken request:\n%s' % (pnr_record_locator, client.request_text))
        log.debug('Calculator PNR %s, broken response:\n%s' % (pnr_record_locator, client.response_text))
    return bookings

if __name__ == '__main__':
    pnr = 'YFCDVY'
    print calc_bookings(pnr)
