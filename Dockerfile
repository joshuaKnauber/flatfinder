FROM python:3.12

WORKDIR /app

COPY . .

# Install Chromium
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -y update

RUN apt-get install -y google-chrome-stable

# Install Requirements
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "index"]
