#!/usr/bin/env python

from .defaults import Constants, Regions, RateLos
import os

Houston = 7100000

if os.environ['SITE'] == 'BCM':

    DEFAULTS = Constants(
        # EDIT YOUR DEFAULTS HERE
        region=Regions(
            houston=Houston,
        ),
        current_hospitalized=6,
        doubling_time=7,
        known_infected=157,
        n_days=60,
        market_share=0.15,
        relative_contact_rate=0.3,
        hospitalized=RateLos(0.025, 7),
        icu=RateLos(0.0075, 9),
        ventilated=RateLos(0.005, 10),
    )
elif os.environ['SITE'] == 'METHODIST':
    DEFAULTS = Constants(
        # EDIT YOUR DEFAULTS HERE
        region=Regions(
            houston=Houston,
        ),
        current_hospitalized=6,
        doubling_time=7,
        known_infected=157,
        n_days=60,
        market_share=0.15,
        relative_contact_rate=0.3,
        hospitalized=RateLos(0.025, 7),
        icu=RateLos(0.0075, 9),
        ventilated=RateLos(0.005, 10),
    )
else:
    raise ValueError(f'Invalid SITE {os.environ["SITE"]}')