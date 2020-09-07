FROM python:3.8-alpine
WORKDIR /root/backend
ENV BASE_URL=https://api.squizz.com/rest/1
ENV ORG_ID=11EA64D91C6E8F70A23EB6800B5BCB6D
ENV API_ORG_KEY=3a62ea5aa2d8845a72dd030369dd571d5123567f70fa76b5bc3bcdf103e3307cc52b01030230c4f2807b44f88ce0052e91f3b7550341f38fe6544d02abfd7d87
ENV API_ORG_PW=Team21_22
ENV MYSQL_DATABASE=squizz_app
# So you don't have to use root, but you can if you like
ENV MYSQL_USERNAME=root
# You can use whatever password you like
ENV MYSQL_PASSWORD=squizz
ENV MYSQL_URI=db
# Password for root access
ENV MYSQL_ROOT_PASSWORD=squizz

# Timezone selection
RUN apk add --no-cache tzdata
ENV TZ=Australia/Melbourne
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apk add build-base
RUN  apk add unixodbc-dev

COPY ./ /root/backend
RUN pip install -r requirements.txt

CMD /bin/sh -c "python -m flask run -h 0.0.0.0 -p 5000"


