# vi: ft=dockerfile

FROM ubuntu:16.04 


# apt dependencies
RUN apt-get update && apt-get install -y \
            python3 python3-pip git \
            libpcre3 libpcre3-dev 


# Copy over ddash
WORKDIR /opt/ddash
COPY . /opt/ddash


# pip dependencies
RUN pip3  install --upgrade pip
RUN pip install -c http://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=stable/queens .
RUN pip install uwsgi


# Set up django
RUN python3 manage.py collectstatic --no-input

EXPOSE 80/tcp

ENTRYPOINT ["uwsgi", "ddash-wsgi.ini"]

