# For more information, please refer to https://aka.ms/vscode-docker-python
FROM coady/pylucene

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 5000

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["python", "search/search.py", "-o", "/indexed"]
#CMD ["python", "query/reddit_query.py"]
CMD ["flask", "run"]