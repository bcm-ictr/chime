#!/usr/bin/env python

from .defaults import Constants, Regions, RateLos

Houston = 7100000

DEFAULTS = Constants(
    # EDIT YOUR DEFAULTS HERE
    region=Houston,
    current_hospitalized=6,
    doubling_time=6,
    known_infected=157,
    n_days=60,
    market_share=0.15,
    relative_contact_rate=0,
    hospitalized=RateLos(0.05, 7),
    icu=RateLos(0.02, 9),
    ventilated=RateLos(0.01, 10),
)
