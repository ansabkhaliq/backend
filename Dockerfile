# FROM python:3.8.6-alpine

# # Timezone selection
# # RUN apk add --no-cache tzdata
# # ENV TZ=Australia/Melbourne
# # RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# # Install Alpine dependencies
# # RUN apk update && apk upgrade
# # RUN apk add build-base
# # RUN apk add unixodbc-dev
# RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev

# # Install requirements
# COPY ./requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy over application source code
# COPY app/ ./

# ENV FLASK_ENV=development

# # Expose container port
# EXPOSE 5000

# # Run the application
# CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"] 

FROM python:3.8-alpine
WORKDIR /root/backend

# Timezone selection
RUN apk add --no-cache tzdata
ENV TZ=Australia/Melbourne
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apk add build-base
RUN apk add unixodbc-dev
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev

COPY ./ /root/backend
RUN pip install -r requirements.txt

CMD /bin/sh -c "python -m flask run -h 0.0.0.0 -p 5000"
