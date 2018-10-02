# vi: ft=dockerfile

FROM ubuntu:16.04 
ARG BUILD=dev


# apt dependencies
RUN apt-get update && apt-get install -y \
            python3 python3-pip git \
            libpcre3 libpcre3-dev 


COPY . /opt/ddash
WORKDIR /opt/ddash


# pip dependencies.
RUN pip3  install --upgrade pip
RUN pip install -c http://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=stable/queens .
RUN pip install uwsgi


# Set up django
RUN python3 manage.py collectstatic --no-input
RUN if [ "$BUILD" = "prod" ]; then ./production_setup.sh; fi


EXPOSE 80/tcp


CMD ["uwsgi", "ddash-wsgi.ini"]

