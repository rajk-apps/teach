FROM python:3.7

ARG APP_NAME
ARG APP_PORT
ARG DJANGO_PROJECT
ARG HOST_IP

ENV APP_NAME=${APP_NAME}
ENV DJANGO_PROJECT=${DJANGO_PROJECT}
ENV DJANGO_HOST=$HOST_IP

COPY ./requirements.txt /requirements.txt
COPY ./start.sh /start.sh
RUN pip install -r requirements.txt
EXPOSE 8888
EXPOSE ${APP_PORT}

RUN django-admin startproject ${DJANGO_PROJECT}
COPY ./deployment/settings_add.py /${DJANGO_PROJECT}/${DJANGO_PROJECT}/settings_add.py
COPY ./deployment/url_add.py /${DJANGO_PROJECT}/${DJANGO_PROJECT}/url_add.py
ENV DJANGO_SETTINGS_MODULE=${DJANGO_PROJECT}.settings_add

CMD ["bash", "/start.sh"]

# manage.py migrate
# manage.py startapp
# python $DJANGO_PROJECT/manage.py runserver 0.0.0.0:6969
# python $DJANGO_PROJECT/manage.py flush -y
# pip install jupyter_contrib_nbextensions