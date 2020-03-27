#!/usr/bin/env python

from .defaults import Constants, Regions, RateLos
import os

Houston = 7100000


# QUOTE: Chris Amos

# According to the website, Harris county has a 43% reduction in travel. I will use that as a metric for base model for BSLMC,
# which I expect matches well the average behavior.  For Harris Health, I will assume 23% reduction in social distancing and for
# Methodist I will assume 63% because I think these two entities serve patient populations that have very different needs and behaviors.

# Attached is screenshot of what I think the baseline model should be for BSLMC with 43% social distancing. 
# For Harris Health I think all is the same except social distancing I will assume to be 23%. For Methodist
# the same but distancing is 63%. Also, perhaps the number of people in the metropolitan Houston area at 
# 4 million is too low? 7.1 M is for Houston+Galveston which is too large. Also I think we should set the 
# baseline model for 30 days not 60. Other parameters should be as indicated. We will have to change 
# number of Hospitalized COVID-19 patients each time.

common_doubling_time = 7
common_n_days = 30

if os.environ['SITE'] == 'BCM':
    DEFAULTS = Constants(
        # EDIT YOUR DEFAULTS HERE
        region=Regions(
            houston=Houston,
        ),
        current_hospitalized=6,
        doubling_time=common_doubling_time,
        known_infected=157,
        n_days=common_n_days,
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
        doubling_time=common_doubling_time,
        known_infected=157,
        n_days=common_n_days,
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
        doubling_time=common_doubling_time,
        known_infected=157,
        n_days=common_n_days,
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
        doubling_time=common_doubling_time,
        known_infected=157,
        n_days=common_n_days,
        market_share=0.15,
        relative_contact_rate=0.23,
        hospitalized=RateLos(0.025, 7),
        icu=RateLos(0.0075, 9),
        ventilated=RateLos(0.005, 10),
    )
else:
    raise ValueError(f'Invalid SITE {os.environ["SITE"]}')
