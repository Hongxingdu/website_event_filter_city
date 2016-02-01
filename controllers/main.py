# -*- coding: utf-8 -*-
# (c) 2016 Vizthoughts Consultancy Ltd. 
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.tools.translate import _

from openerp.addons.website_event.controllers.main import website_event


class WebsiteEventCity(website_event):

    @http.route(
        ['/event', '/event/page/<int:page>'],
        type='http', auth="public", website=True)
    def events(self, page=1, **searches):
        response = super(WebsiteEventCity, self).events(page, **searches)
        current_city = None

        searches.update(response.qcontext['searches'])
        searches.setdefault('city', 'all')

        event_obj = request.env['event.event']
        events = response.qcontext['event_ids']

        cities = event_obj.read_group(
            [('id', 'in', events.ids)], [' city_id'], 'city_id')
        cities.insert(0, {
            'city_id_count': len(events),
            'city_id': ("all", _("All Cities"))
        })

        if searches['city'] != 'all':
            events = events.filtered(
                lambda x: x.city_id.id == int(searches["city"]))
            current_city = \
                events and events[0].sudo().city_id.name or ''

        step = 10  # events per page
        pager = request.website.pager(
            url="/event",
            url_args={
                'date': searches.get('date'),
                'type': searches.get('type'),
                'country': searches.get('country'),
                'city': searches.get('city'),
            },
            total=len(events),
            page=page,
            step=step,
            scope=5)
        offset = response.qcontext['pager']['offset']
        events = events[offset:offset+step]

        response.qcontext.update({
            'current_city': current_city,
            'Cities': cities,
            'event_ids': events,
            'searches': searches,
            'pager': pager,
        })
        return response
