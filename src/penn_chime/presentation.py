"""effectful functions for streamlit io"""
import os
from typing import Optional
from datetime import date

import altair as alt
import numpy as np
import pandas as pd

from .constants import (
    CHANGE_DATE,
    DATE_FORMAT,
    DOCS_URL,
    FLOAT_INPUT_MIN,
    FLOAT_INPUT_STEP,
)

from .utils import dataframe_to_base64
from .parameters import Parameters, Disposition
from .models import SimSirModel as Model

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """


########
# Text #
########


def display_header(st, m, p):
#     <link rel="stylesheet" href="https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css">
# <div class="penn-medicine-header__content">
#     <a href="https://www.pennmedicine.org" class="penn-medicine-header__logo"
#         title="Go to the Penn Medicine home page">Penn Medicine</a>
#     <a id="title" class="penn-medicine-header__title">Penn Medicine - COVID-19 Hospital Impact Model for Epidemics</a>
# </div>

    if os.environ['SITE'] == 'TCH':
        st.markdown(
        """
<div class="penn-medicine-header__content">
    <a href="https://www.bcm.edu"
        title="Go to the BCM home page"><img valign="top" width="120" height="120" src="https://media.bcm.edu/images/2016/0d/logo-bcm-flat.png"></a>
    <h1>TCH - COVID-19 Hospital Impact Model for Epidemics
    <a href="https://www.texaschildrens.org/"
        title="Go to the TCH home page"><img valign="top" width="120" height="120" src="https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-original-577x577/s3/052012/texas-childrens.jpg"></a>
        </h1>
</div>
    """,
        unsafe_allow_html=True,
    )
    elif os.environ['SITE'] == 'METHODIST':
        st.markdown(
        """
    <div class="penn-medicine-header__content">
    <a href="https://www.bcm.edu/"
        title="Go to the BCM home page"><img valign="top" height="120"
        src="https://media.bcm.edu/images/2016/0d/logo-bcm-flat.png"></a>
    <h1>Methodist - COVID-19 Hospital Impact Model for Epidemics<a href="https://www.houstonmethodist.org/"
        title="Go to the Methodist home page"><img valign="top" height="64"
        src="https://www.houstonmethodist.org/-/media/Images/Header-Images/logo.ashx?h=72&w=216&hash=C4A85BF6D599BC04FE120E1FE46B9BE0"></a>
        </h1>
</div>
    """,
        unsafe_allow_html=True,
    )
    elif os.environ['SITE'] == 'BSLMC':
            st.markdown(
        """
    <div class="penn-medicine-header__content">
    <a href="https://www.bcm.edu/"
        title="Go to the BCM home page"><img valign="top" height="120"
        src="https://media.bcm.edu/images/2016/0d/logo-bcm-flat.png"></a>
    <h1>BSLMC - COVID-19 Hospital Impact Model for Epidemics<a href="https://www.chistlukeshealth.org/"
        title="Go to the Methodist home page"><img valign="top" height="64"
        src="https://www.chistlukeshealth.org/sites/default/files/chi_logo_svg.svg"></a>
        </h1>
</div>
    """,
        unsafe_allow_html=True,
    )
    elif os.environ['SITE'] == 'HarrisHealth':
            st.markdown(
        """
    <div class="penn-medicine-header__content">
    <a href="https://www.bcm.edu/"
        title="Go to the BCM home page"><img valign="top" height="120"
        src="https://media.bcm.edu/images/2016/0d/logo-bcm-flat.png"></a>
    <h1>HarrisHealth - COVID-19 Hospital Impact Model for Epidemics<a href="https://www.harrishealth.org/"
        title="Go to the Methodist home page"><img valign="top" height="64"
        src="https://www.harrishealth.org/_catalogs/masterpage/HHSInternet/assets/client/assets/logo.jpg"></a>
        </h1>
</div>
    """,
        unsafe_allow_html=True,
    )
    elif os.environ['SITE'] == 'HoustonVA':
            st.markdown(
        """
    <div class="penn-medicine-header__content">
    <a href="https://www.bcm.edu/"
        title="Go to the BCM home page"><img valign="top" height="120"
        src="https://media.bcm.edu/images/2016/0d/logo-bcm-flat.png"></a>
    <h1>Houston VA - COVID-19 Hospital Impact Model for Epidemics<a href="https://www.houston.va.gov/"
        title="Go to the Houston VA home page"><img valign="top" height="120"
        src="https://www.epilepsy.va.gov/SouthWest/Houston/houston_logo_sm.JPG"></a>
        </h1>
</div>
    """,
        unsafe_allow_html=True,
    )
    elif os.environ['SITE'] == 'NationalVA':
            st.markdown(
        """
    <div class="penn-medicine-header__content">
    <a href="https://www.bcm.edu/"
        title="Go to the BCM home page"><img valign="top" height="120"
        src="https://media.bcm.edu/images/2016/0d/logo-bcm-flat.png"></a>
    <h1>National VA - COVID-19 Hospital Impact Model for Epidemics<a href="https://www.va.gov/"
        title="Go to the National VA home page"><img valign="top" height="120"
        src="https://www.va.gov/img/design/logo/va-logo.png"></a>
        </h1>
</div>
    """,
        unsafe_allow_html=True,
    )
    else:
        raise ValueError(f"Invalid SITE {os.environ['SITE']}")

    # st.markdown("""
    #     All sites: [TCH](http://0.0.0.0:8000), [Methodist](http://0.0.0.0:8001)
    # """)
    # st.markdown(
    #     """**IMPORTANT NOTICE**: Admissions and Census calculations were previously **undercounting**. Please update your reports generated before """ + p.change_date() + """. See more about changes [here](https://github.com/CodeForPhilly/chime/labels/models)."""
    # )

    infection_warning_str = ''
    infected_population_warning_str = ''
    st.markdown(
        """The estimated number of currently infected individuals is **{total_infections:.0f}**. This is based on current inputs for
    Hospitalizations (**{current_hosp}**), Hospitalization rate (**{hosp_rate:.0%}**), Region size (**{S}**),
    and Hospital market share (**{market_share:.0%}**).

{infected_population_warning_str}

An initial doubling time of **{doubling_time}** days and a recovery time of **{recovery_days}** days imply an $R_0$ of
 **{r_naught:.2f}** and daily growth rate of **{daily_growth:.2f}%**.

**Mitigation**: A **{relative_contact_rate:.0%}** reduction in social contact after the onset of the
outbreak **{impact_statement:s} {doubling_time_t:.1f}** days, implying an effective $R_t$ of **${r_t:.2f}$**
and daily growth rate of **{daily_growth_t:.2f}%**.
""".format(
            total_infections=m.infected,
            current_hosp=p.current_hospitalized,
            hosp_rate=p.hospitalized.rate,
            S=p.population,
            market_share=p.market_share,
            recovery_days=p.infectious_days,
            r_naught=m.r_naught,
            doubling_time=p.doubling_time,
            relative_contact_rate=p.relative_contact_rate,
            r_t=m.r_t,
            doubling_time_t=abs(m.doubling_time_t),
            impact_statement=(
                "halves the infections every"
                if m.r_t < 1
                else "reduces the doubling time to"
            ),
            daily_growth=m.daily_growth_rate * 100.0,
            daily_growth_t=m.daily_growth_rate_t * 100.0,
            infected_population_warning_str=infected_population_warning_str,
        )
    )

    return None


class Input:
    """Helper to separate Streamlit input definition from creation/rendering"""

    def __init__(self, st_obj, label, value, kwargs):
        self.st_obj = st_obj
        self.label = label
        self.value = value
        self.kwargs = kwargs

    def __call__(self):
        return self.st_obj(self.label, value=self.value, **self.kwargs)


class NumberInput(Input):
    def __init__(
        self,
        st_obj,
        label,
        min_value=None,
        max_value=None,
        value=None,
        step=None,
        format=None,
        key=None,
    ):
        kwargs = dict(
            min_value=min_value, max_value=max_value, step=step, format=format, key=key
        )
        super().__init__(st_obj.number_input, label, value, kwargs)


class DateInput(Input):
    def __init__(self, st_obj, label, value=None, key=None):
        kwargs = dict(key=key)
        super().__init__(st_obj.date_input, label, value, kwargs)


class PercentInput(NumberInput):
    def __init__(
        self,
        st_obj,
        label,
        min_value=0.0,
        max_value=100.0,
        value=None,
        step=FLOAT_INPUT_STEP,
        format="%f",
        key=None,
    ):
        super().__init__(
            st_obj, label, min_value, max_value, value * 100.0, step, format, key
        )

    def __call__(self):
        return super().__call__() / 100.0


class CheckboxInput(Input):
    def __init__(self, st_obj, label, value=None, key=None):
        kwargs = dict(key=key)
        super().__init__(st_obj.checkbox, label, value, kwargs)


def display_sidebar(st, d: Parameters) -> Parameters:
    # Initialize variables
    # these functions create input elements and bind the values they are set to
    # to the variables they are set equal to
    # it's kindof like ember or angular if you are familiar with those

    st_obj = st.sidebar
    current_hospitalized_input = NumberInput(
        st_obj,
        "Currently Hospitalized COVID-19 Patients",
        min_value=0,
        value=d.current_hospitalized,
        step=1,
        format="%i",
    )
    n_days_input = NumberInput(
        st_obj,
        "Number of days to project",
        min_value=30,
        value=d.n_days,
        step=1,
        format="%i",
    )
    doubling_time_input = NumberInput(
        st_obj,
        "Doubling time in days (up to today)",
        min_value=0.5,
        value=d.doubling_time,
        step=0.25,
        format="%f",
    )
    current_date_input = DateInput(
        st_obj, "Current date (Default is today)", value=d.current_date,
    )
    date_first_hospitalized_input = DateInput(
        st_obj, "Date of first hospitalized case - Enter this date to have chime estimate the initial doubling time",
        value=d.date_first_hospitalized,
    )
    relative_contact_pct_input = PercentInput(
        st_obj,
        "Social distancing (% reduction in social contact going forward)",
        min_value=0.0,
        max_value=100.0,
        value=d.relative_contact_rate,
        step=1.0,
    )
    hospitalized_pct_input = PercentInput(
        st_obj, "Hospitalization %(total infections)", value=d.hospitalized.rate,
    )
    icu_pct_input = PercentInput(st_obj,
        "ICU %(total infections)",
        min_value=0.0,
        value=d.icu.rate,
        step=0.05
    )
    ventilated_pct_input = PercentInput(
        st_obj, "Ventilated %(total infections)", value=d.ventilated.rate,
    )
    hospitalized_days_input = NumberInput(
        st_obj,
        "Average Hospital Length of Stay (days)",
        min_value=0,
        value=d.hospitalized.days,
        step=1,
        format="%i",
    )
    icu_days_input = NumberInput(
        st_obj,
        "Average Days in ICU",
        min_value=0,
        value=d.icu.days,
        step=1,
        format="%i",
    )
    ventilated_days_input = NumberInput(
        st_obj,
        "Average Days on Ventilator",
        min_value=0,
        value=d.ventilated.days,
        step=1,
        format="%i",
    )
    market_share_pct_input = PercentInput(
        st_obj,
        "Hospital Market Share (%)",
        min_value=0.5,
        value=d.market_share,
    )
    population_input = NumberInput(
        st_obj,
        "Regional Population",
        min_value=1,
        value=(d.population),
        step=1,
        format="%i",
    )
    infectious_days_input = NumberInput(
        st_obj,
        "Infectious Days",
        min_value=0,
        value=d.infectious_days,
        step=1,
        format="%i",
    )
    max_y_axis_set_input = CheckboxInput(
        st_obj, "Set the Y-axis on graphs to a static value"
    )
    max_y_axis_input = NumberInput(
        st_obj, "Y-axis static value", value=500, format="%i", step=25
    )

    # Build in desired order
    st.sidebar.markdown(
        """**CHIME [v1.1.2](https://github.com/CodeForPhilly/chime/releases/tag/v1.1.1) ({change_date})**""".format(
            change_date=CHANGE_DATE
        )
    )

    st.sidebar.markdown(
        "### Hospital Parameters [ℹ]({docs_url}/what-is-chime/parameters#hospital-parameters)".format(
            docs_url=DOCS_URL
        )
    )
    population = population_input()
    market_share = market_share_pct_input()
    # known_infected = known_infected_input()
    current_hospitalized = current_hospitalized_input()

    st.sidebar.markdown(
        "### Spread and Contact Parameters [ℹ]({docs_url}/what-is-chime/parameters#spread-and-contact-parameters)".format(
            docs_url=DOCS_URL
        )
    )

    if st.sidebar.checkbox(
        "I know the date of the first hospitalized case."
    ):
        date_first_hospitalized = date_first_hospitalized_input()
        doubling_time = None
    else:
        doubling_time = doubling_time_input()
        date_first_hospitalized = None

    relative_contact_rate = relative_contact_pct_input()

    st.sidebar.markdown(
        "### Severity Parameters [ℹ]({docs_url}/what-is-chime/parameters#severity-parameters)".format(
            docs_url=DOCS_URL
        )
    )
    hospitalized_rate = hospitalized_pct_input()
    icu_rate = icu_pct_input()
    ventilated_rate = ventilated_pct_input()
    infectious_days = infectious_days_input()
    hospitalized_days = hospitalized_days_input()
    icu_days = icu_days_input()
    ventilated_days = ventilated_days_input()

    st.sidebar.markdown(
        "### Display Parameters [ℹ]({docs_url}/what-is-chime/parameters#display-parameters)".format(
            docs_url=DOCS_URL
        )
    )
    n_days = n_days_input()
    max_y_axis_set = max_y_axis_set_input()

    max_y_axis = None
    if max_y_axis_set:
        max_y_axis = max_y_axis_input()

    current_date = current_date_input()

    return Parameters(
        current_hospitalized=current_hospitalized,
        hospitalized=Disposition(hospitalized_rate, hospitalized_days),
        icu=Disposition(icu_rate, icu_days),
        relative_contact_rate=relative_contact_rate,
        ventilated=Disposition(ventilated_rate, ventilated_days),
        current_date=current_date,
        date_first_hospitalized=date_first_hospitalized,
        doubling_time=doubling_time,
        infectious_days=infectious_days,
        market_share=market_share,
        max_y_axis=max_y_axis,
        n_days=n_days,
        population=population,
    )

def show_references_used(st, model, parameters, defaults, notes: str=""):
    st.subheader(
        "References used for the default parameters"
    )
    st.markdown(
        '''\
* [Clinical Characteristics of 138 Hospitalized Patients With 2019 Novel Coronavirus–Infected Pneumonia in Wuhan, China](https://jamanetwork.com/journals/jama/fullarticle/2761044)
  shows 10 days as hospital length of stay for Wuhan. We will use this parameter as default before data from local hospitcals become available.

* [Impact of non-pharmaceutical interventions (NPIs) to reduce COVID19 mortality and healthcare demand](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-College-COVID19-NPI-modelling-16-03-2020.pdf) by Ferguson et al The actual social distancing
  analysis that is posted by CHIME is not all that relevant to my mind with the Houston environment because it seems almost exclusively
  focused on impact of social distancing for children and more of the impact here is on businesses (schools are all shut so the impact
  on kids is nearly 100% social distancing for them except through family environments) The family environments in Houston are much more
  permissive to spread than I expect they are in the UK. I think distance traveled is a good overall metric.

* [Covid-19 Social Distancing Scoreboard - Unacast](https://www.unacast.com/covid19/social-distancing-scoreboard)
  According to the website, Harris county has a 43% reduction in travel. I will use that as a metric for base model for BSLMC,
  which I expect matches well the average behavior.  For Harris Health, I will assume 23% reduction in social distancing and for
  Methodist I will assume 63% because I think these two entities serve patient populations that have very different needs and behaviors.

* [Estimates of the severity of COVID-19 disease](https://www.medrxiv.org/content/10.1101/2020.03.09.20033357v1)

* [Projecting the Impact of the SARS-CoV-2 in TMC](https://rdl-covdws-p01.ad.bcm.edu/sites/default/files/2020-04/Projecting%20the%20Impact%20of%20the%20SARS-CoV-2%20in%20TMC.pptx)
        '''
    )

def display_more_info(
    st, model: Model, parameters: Parameters, defaults: Parameters, notes: str = "",
):
    """a lot of streamlit writing to screen."""
    st.subheader(
        "[Discrete-time SIR modeling](https://mathworld.wolfram.com/SIRModel.html) of infections/recovery"
    )
    st.markdown(
        """The model consists of individuals who are either _Susceptible_ ($S$), _Infected_ ($I$), or _Recovered_ ($R$).

The epidemic proceeds via a growth and decline process. This is the core model of infectious disease spread and has been in use in epidemiology for many years."""
    )
    st.markdown("""The dynamics are given by the following 3 equations.""")

    st.latex("S_{t+1} = (-\\beta S_t I_t) + S_t")
    st.latex("I_{t+1} = (\\beta S_t I_t - \\gamma I_t) + I_t")
    st.latex("R_{t+1} = (\\gamma I_t) + R_t")

    st.markdown(
        """To project the expected impact to Penn Medicine, we estimate the terms of the model.

To do this, we use a combination of estimates from other locations, informed estimates based on logical reasoning, and best guesses from the American Hospital Association.


### Parameters

The model's parameters, $\\beta$ and $\\gamma$, determine the virulence of the epidemic.

$$\\beta$$ can be interpreted as the _effective contact rate_:
"""
    )
    st.latex("\\beta = \\tau \\times c")

    st.markdown(
        """which is the transmissibility ($\\tau$) multiplied by the average number of people exposed ($$c$$).  The transmissibility is the basic virulence of the pathogen.  The number of people exposed $c$ is the parameter that can be changed through social distancing.


$\\gamma$ is the inverse of the mean recovery time, in days.  I.e.: if $\\gamma = 1/{recovery_days}$, then the average infection will clear in {recovery_days} days.

An important descriptive parameter is the _basic reproduction number_, or $R_0$.  This represents the average number of people who will be infected by any given infected person.  When $R_0$ is greater than 1, it means that a disease will grow.  Higher $R_0$'s imply more rapid growth.  It is defined as """.format(
            recovery_days=int(parameters.infectious_days)
        )
    )
    st.latex("R_0 = \\beta /\\gamma")

    st.markdown(
        """

$R_0$ gets bigger when

- there are more contacts between people
- when the pathogen is more virulent
- when people have the pathogen for longer periods of time

A doubling time of {doubling_time} days and a recovery time of {recovery_days} days imply an $R_0$ of {r_naught:.2f}.

#### Effect of social distancing

After the beginning of the outbreak, actions to reduce social contact will lower the parameter $c$.  If this happens at
time $t$, then the number of people infected by any given infected person is $R_t$, which will be lower than $R_0$.

A {relative_contact_rate:.0%} reduction in social contact would increase the time it takes for the outbreak to double,
to {doubling_time_t:.2f} days from {doubling_time:.2f} days, with a $R_t$ of {r_t:.2f}.

#### Using the model

We need to express the two parameters $\\beta$ and $\\gamma$ in terms of quantities we can estimate.

- $\\gamma$:  the CDC is recommending 14 days of self-quarantine, we'll use $\\gamma = 1/{recovery_days}$.
- To estimate $$\\beta$$ directly, we'd need to know transmissibility and social contact rates.  since we don't know these things, we can extract it from known _doubling times_.  The AHA says to expect a doubling time $T_d$ of 7-10 days. That means an early-phase rate of growth can be computed by using the doubling time formula:
""".format(
            doubling_time=parameters.doubling_time,
            recovery_days=parameters.infectious_days,
            r_naught=model.r_naught,
            relative_contact_rate=parameters.relative_contact_rate,
            doubling_time_t=model.doubling_time_t,
            r_t=model.r_t,
        )
    )
    st.latex("g = 2^{1/T_d} - 1")

    st.markdown(
        """
- Since the rate of new infections in the SIR model is $g = \\beta S - \\gamma$, and we've already computed $\\gamma$, $\\beta$ becomes a function of the initial population size of susceptible individuals.
$$\\beta = (g + \\gamma)$$.


### Initial Conditions

- {notes} \n
""".format(
            notes=notes
        )
    )
    return None


def write_definitions(st):
    st.subheader("Guidance on Selecting Inputs")
    st.markdown(
        """**This information has been moved to the
[User Documentation]({docs_url}/what-is-chime/parameters)**""".format(
            docs_url=DOCS_URL
        )
    )


def write_footer(st):
    st.subheader("References & Acknowledgements")
    st.markdown(
        """* AHA Webinar, Feb 26, James Lawler, MD, an associate professor University of Nebraska Medical Center, What Healthcare Leaders Need To Know: Preparing for the COVID-19
* We would like to recognize the valuable assistance in consultation and review of model assumptions by Michael Z. Levy, PhD, Associate Professor of Epidemiology, Department of Biostatistics, Epidemiology and Informatics at the Perelman School of Medicine
* Finally we'd like to thank [Code for Philly](https://codeforphilly.org/) and the many members of the open-source community that [contributed](https://github.com/CodeForPhilly/chime/graphs/contributors) to this project.
    """
    )
    st.markdown(
        """*This tool was originally developed by the [Predictive Healthcare team](http://predictivehealthcare.pennmedicine.org/) at
    Penn Medicine. For questions on how to use this tool see the [User docs](https://code-for-philly.gitbook.io/chime/). Code can be found on [Github](https://github.com/CodeForPhilly/chime).
    Join our [Slack channel](https://codeforphilly.org/chat?channel=covid19-chime-penn) if you would like to get involved!*"""
    )
    st.markdown("""© 2020, This work is derived from the [CodeForPhilly/chime](chime) project from the University of Pennsylvania,
    and has been adapted for the Greater Houston Area by [the Institute for Clinical and Translational Research at the Baylor College of Medicine](https://www.bcm.edu/research/office-of-research/clinical-and-translational-research).""")

#     <link rel="stylesheet" href="https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css">
# <div class="penn-medicine-header__content">
#     <a href="https://www.pennmedicine.org" class="penn-medicine-header__logo"
#         title="Go to the Penn Medicine home page">Penn Medicine</a>
#     <a id="title" class="penn-medicine-header__title">Penn Medicine - COVID-19 Hospital Impact Model for Epidemics</a>
# </div>


def display_download_link(st, filename: str, df: pd.DataFrame):
    csv = dataframe_to_base64(df)
    st.markdown(
        """
        <a download="{filename}" href="data:file/csv;base64,{csv}">Download {filename}</a>
""".format(
            csv=csv, filename=filename
        ),
        unsafe_allow_html=True,
    )
