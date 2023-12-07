# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN apt-get update && apt-get install -y unzip

# Japanese Localization
RUN cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# google-chrome
RUN curl -O https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -yq --no-install-recommends ./google-chrome-stable_current_amd64.deb && \
    apt-get clean && rm google-chrome-stable_current_amd64.deb

# ChromeDriver
ADD https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.62/linux64/chromedriver-linux64.zip /opt/chrome/
RUN cd /opt/chrome/ && unzip chromedriver-linux64.zip

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# https://q-three.com/archives/1031
# https://qiita.com/otomaru97/items/6f7d9ebb5e4187cf8505
# https://blog.shikoan.com/chrome-drive-binary/
# https://qiita.com/tru-y/items/49455a24c29498f24aa9

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/chrome
