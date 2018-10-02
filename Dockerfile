# vi: ft=dockerfile

FROM ubuntu:16.04 
ARG BUILD=dev


# apt dependencies
RUN apt-get update && apt-get install -y \
            python3 python3-pip git \
            libpcre3 libpcre3-dev 


# pip dependencies.
# NB: Copying requirements and setup files for better build caching.
WORKDIR /opt/ddash
COPY requirements.txt /opt/ddash/requirements.txt
COPY setup.py /opt/ddash/setup.py
COPY openstack_dashboard/hooks.py /opt/ddash/openstack_dashboard/hooks.py
COPY horizon* /opt/ddash/
COPY README.rst /opt/ddash/README.rst
COPY setup.cfg /opt/ddash/setup.cfg

RUN pip3  install --upgrade pip
RUN pip install -c http://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=stable/queens .
RUN pip install uwsgi


# Now copy everything else
COPY . /opt/ddash


# Set up django
RUN python3 manage.py collectstatic --no-input
RUN if [ "$BUILD" = "prod" ]; then ./production_setup.sh; fi


EXPOSE 80/tcp


CMD ["uwsgi", "ddash-wsgi.ini"]

