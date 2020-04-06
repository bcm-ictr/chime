#!/usr/bin/env python
import os
from datetime import date

from .parameters import Parameters, Regions, Disposition


def get_defaults():

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

    common_doubling_time = 6.0
    common_n_days = 150
    common_hospital_length_of_stay = 8
    common_hospitalization_rate = 0.044    # 0.044 means 4.4%
    common_icu_rate = 0.0215
    common_icu_legnth_of_stay = 12
    common_ventilated_rate = 0.0145
    common_ventilated_length_of_stay = 11


    Houston_population_size = 4698619

    #
    # NOTE: RateLos is rate + length of stay.
    #
    if os.environ['SITE'] == 'TCH':
        return Parameters(
            population=Houston_population_size,
            current_hospitalized=86,
            # NO LONGER NEEDED?
            #known_infected=157,
            # NEW PARAMETER
            date_first_hospitalized=date(2020,3,7),
            #
            doubling_time=common_doubling_time,
            hospitalized=Disposition(common_hospitalization_rate, common_hospital_length_of_stay),
            icu=Disposition(common_icu_rate, common_icu_legnth_of_stay),
            infectious_days=14,
            market_share=0.0471,
            n_days=common_n_days,
            relative_contact_rate=0.30,
            ventilated=Disposition(common_ventilated_rate, common_ventilated_length_of_stay),
        )
    elif os.environ['SITE'] == 'METHODIST':
        return Parameters(
            population=Houston_population_size,
            current_hospitalized=86,
            # NO LONGER NEEDED?
            #known_infected=157,
            # NEW PARAMETER
            date_first_hospitalized=date(2020,3,7),
            #
            doubling_time=common_doubling_time,
            hospitalized=Disposition(common_hospitalization_rate, common_hospital_length_of_stay),
            icu=Disposition(common_icu_rate, common_icu_legnth_of_stay),
            infectious_days=14,
            market_share=0.0601,
            n_days=common_n_days,
            relative_contact_rate=0.30,
            ventilated=Disposition(common_ventilated_rate, common_ventilated_length_of_stay),
        )
    elif os.environ['SITE'] == 'BSLMC':
        return Parameters(
            population=Houston_population_size,
            current_hospitalized=86,
            # NO LONGER NEEDED?
            #known_infected=157,
            # NEW PARAMETER
            date_first_hospitalized=date(2020,3,7),
            #
            doubling_time=common_doubling_time,
            hospitalized=Disposition(common_hospitalization_rate, common_hospital_length_of_stay),
            icu=Disposition(common_icu_rate, common_icu_legnth_of_stay),
            infectious_days=14,
            market_share=0.0348,
            n_days=common_n_days,
            relative_contact_rate=0.30,
            ventilated=Disposition(common_ventilated_rate, common_ventilated_length_of_stay),
        )
    elif os.environ['SITE'] == 'HarrisHealth':
        return Parameters(
            population=Houston_population_size,
            current_hospitalized=86,
            # NO LONGER NEEDED?
            #known_infected=157,
            # NEW PARAMETER
            date_first_hospitalized=date(2020,3,7),
            #
            doubling_time=common_doubling_time,
            hospitalized=Disposition(common_hospitalization_rate, common_hospital_length_of_stay),
            icu=Disposition(common_icu_rate, common_icu_legnth_of_stay),
            infectious_days=14,
            market_share=0.0365,
            n_days=common_n_days,
            relative_contact_rate=0.30,
            ventilated=Disposition(common_ventilated_rate, common_ventilated_length_of_stay),
        )
    elif os.environ['SITE'] == 'HoustonVA':
        return Parameters(
            population=Houston_population_size,
            current_hospitalized=86,
            # NO LONGER NEEDED?
            #known_infected=157,
            # NEW PARAMETER
            date_first_hospitalized=date(2020,3,7),
            #
            doubling_time=common_doubling_time,
            hospitalized=Disposition(common_hospitalization_rate, common_hospital_length_of_stay),
            icu=Disposition(common_icu_rate, common_icu_legnth_of_stay),
            infectious_days=14,
            market_share=0.03,
            n_days=common_n_days,
            relative_contact_rate=0.30,
            ventilated=Disposition(common_ventilated_rate, common_ventilated_length_of_stay),
        )
    elif os.environ['SITE'] == 'NationalVA':
        return Parameters(
            population=Houston_population_size,
            current_hospitalized=86,
            # NO LONGER NEEDED?
            #known_infected=157,
            # NEW PARAMETER
            date_first_hospitalized=date(2020,3,7),
            #
            doubling_time=common_doubling_time,
            hospitalized=Disposition(common_hospitalization_rate, common_hospital_length_of_stay),
            icu=Disposition(common_icu_rate, common_icu_legnth_of_stay),
            infectious_days=14,
            market_share=0.03,
            n_days=common_n_days,
            relative_contact_rate=0.30,
            ventilated=Disposition(common_ventilated_rate, common_ventilated_length_of_stay),
        )
    else:
        raise ValueError(f'Invalid SITE {os.environ["SITE"]}')

