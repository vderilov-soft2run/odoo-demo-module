FROM python:3.11.9

ARG PGDATABASE
ARG PGPASSWORD
ARG PGUSER
ARG PGHOST

ENV PGDATABASE=${PGDATABASE}
ENV PGPASSWORD=${PGPASSWORD}
ENV PGUSER=${PGUSER}
ENV PGHOST=${PGHOST}


RUN apt-get update
RUN apt-get install -y python3-dev libxml2-dev \
    libxslt1-dev zlib1g-dev libsasl2-dev \ 
    libldap2-dev build-essential libssl-dev \ 
    libffi-dev libjpeg-dev \ 
    libpq-dev liblcms2-dev \ 
    libblas-dev libatlas-base-dev 

RUN useradd -ms /bin/bash odoo_adm
USER odoo_adm

COPY ./ /home/odoo_adm/odoo/

WORKDIR /home/odoo_adm/odoo/

RUN mkdir /home/odoo_adm/data

RUN pip install -r requirements.txt

CMD ./odoo-bin --addons-path="addons/" -r $PGUSER -w $PGPASSWORD -d $PGDATABASE --db_host $PGHOST -i base --dev=reload