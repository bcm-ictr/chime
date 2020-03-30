"""App."""

import altair as alt  # type: ignore
import streamlit as st  # type: ignore
import os

from penn_chime.presentation import (
    build_download_link,
    display_header,
    display_sidebar,
    draw_census_table,
    draw_projected_admissions_table,
    draw_raw_sir_simulation_table,
    hide_menu_style,
    show_additional_projections,
    show_references_used,
    show_more_info_about_this_tool,
    write_definitions,
    write_footer,
)
from penn_chime.settings import DEFAULTS
from penn_chime.models import SimSirModel
from penn_chime.charts import (
    additional_projections_chart,
    admitted_patients_chart,
    new_admissions_chart,
    chart_descriptions
)

# This is somewhat dangerous:
# Hide the main menu with "Rerun", "run on Save", "clear cache", and "record a screencast"
# This should not be hidden in prod, but removed
# In dev, this should be shown
st.markdown(hide_menu_style, unsafe_allow_html=True)

p = display_sidebar(st, DEFAULTS)
m = SimSirModel(p)

display_header(st, m, p)


if st.checkbox("Show references that we used to justify the default parameters"):
    notes = "We used information from ... to justify the default parameters"
    show_references_used(st=st, model=m, parameters=p, defaults=DEFAULTS, notes=notes)

if st.checkbox("Show more info about this tool"):
    notes = "The total size of the susceptible population will be the entire catchment area for Penn Medicine entities (HUP, PAH, PMC, CCH)"
    show_more_info_about_this_tool(st=st, model=m, parameters=p, defaults=DEFAULTS, notes=notes)

st.subheader("New Admissions")
st.markdown("Projected number of **daily** COVID-19 admissions at {} hospitals".format(os.environ['SITE']))
new_admit_chart = new_admissions_chart(alt, m.admits_df, parameters=p)
st.altair_chart(
    new_admissions_chart(alt, m.admits_df, parameters=p),
    use_container_width=True,
)

st.markdown(chart_descriptions(new_admit_chart, p.labels))

if st.checkbox("Show Projected Admissions in tabular form"):
    if st.checkbox("Show Daily Counts"):
        draw_projected_admissions_table(st, m.admits_df, p.labels, 1, as_date=p.as_date)
    else:
        admissions_day_range = st.slider(
            label="Interval of Days",
            key="admissions_day_range_slider",
            min_value=1,
            max_value=10,
            value=7 
        )
        draw_projected_admissions_table(st, m.admits_df, p.labels, admissions_day_range, as_date=p.as_date)
    build_download_link(st,
        filename="projected_admissions.csv",
        df=m.admits_df,
        parameters=p
    )
st.subheader("Admitted Patients (Census)")
st.markdown(
    "Projected **census** of COVID-19 patients, accounting for arrivals and discharges at {} hospitals".format(os.environ['SITE'])
)
census_chart = admitted_patients_chart(alt=alt, census=m.census_df, parameters=p)
st.altair_chart(
    admitted_patients_chart(alt=alt, census=m.census_df, parameters=p),
    use_container_width=True,
)
st.markdown(chart_descriptions(census_chart, p.labels, suffix=" Census"))
if st.checkbox("Show Projected Census in tabular form"):
    if st.checkbox("Show Daily Census Counts"):
        draw_census_table(st, m.census_df, p.labels, 1, as_date=p.as_date)
    else:
        census_day_range = st.slider(
            label='Interval of Days',
            key="census_day_range_slider",
            min_value=1,
            max_value=10,
            value=7 
        )
        draw_census_table(st, m.census_df, p.labels, census_day_range, as_date=p.as_date)
    build_download_link(st,
        filename="projected_census.csv",
        df=m.census_df,
        parameters=p
    )

st.markdown(
    """**Click the checkbox below to view additional data generated by this simulation**"""
)
if st.checkbox("Show Additional Projections"):
    show_additional_projections(
        st, alt, additional_projections_chart, model=m, parameters=p
    )
    if st.checkbox("Show Raw SIR Simulation Data"):
        draw_raw_sir_simulation_table(st, model=m, parameters=p)
write_definitions(st)
write_footer(st)
