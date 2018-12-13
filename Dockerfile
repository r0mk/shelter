FROM python:2
ADD gspreadsheet_notifier.py /
ADD token.json /
ADD credentials.json /
RUN apt-get update && apt-get install tor -y
RUN pip install google-api-python-client oauth2client requests PySocks
CMD /etc/init.d/tor start && python /gspreadsheet_notifier.py 
#CMD [ "python", "./gspreadsheet_notifier.py" ]
