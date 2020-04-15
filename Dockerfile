FROM python:3.7.7-slim-buster
ARG SITE
ENV PARAMETERS=./defaults/webapp-$SITE.cfg
WORKDIR /app
COPY README.md .
COPY setup.cfg .
COPY setup.py .
COPY .streamlit .streamlit
COPY defaults defaults
COPY src src
RUN pip install -q .

CMD ["streamlit", "run", "src/app.py"]

