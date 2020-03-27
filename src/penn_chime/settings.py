#!/usr/bin/env python

from .defaults import Constants, Regions, RateLos
import os

Houston = 7100000


# QUOTE: Chris Amos

# According to the website, Harris county has a 43% reduction in travel. I will use that as a metric for base model for BSLMC,
# which I expect matches well the average behavior.  For Harris Health, I will assume 23% reduction in social distancing and for
# Methodist I will assume 63% because I think these two entities serve patient populations that have very different needs and behaviors.

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
        relative_contact_rate=0.63,
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
        relative_contact_rate=0.63,
        hospitalized=RateLos(0.025, 7),
        icu=RateLos(0.0075, 9),
        ventilated=RateLos(0.005, 10),
    )
elif os.environ['SITE'] == 'BSLMC':
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
        relative_contact_rate=0.43,
        hospitalized=RateLos(0.025, 7),
        icu=RateLos(0.0075, 9),
        ventilated=RateLos(0.005, 10),
    )
elif os.environ['SITE'] == 'HarrisHealth':
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
        relative_contact_rate=0.23,
        hospitalized=RateLos(0.025, 7),
        icu=RateLos(0.0075, 9),
        ventilated=RateLos(0.005, 10),
    )
else:
    raise ValueError(f'Invalid SITE {os.environ["SITE"]}')