#FROM python:3.6.7-alpine3.6
FROM python:3

# author of file
LABEL maintainer = ”YBA <burakakkas55@gmail.com>”

WORKDIR /app

# Packages that we need
COPY requirements.txt /app

# instruction to be run during image build
RUN pip install -r requirements.txt


# We want to start app.py file. (change it with your file name)

# Argument to python command
#CMD ["python", “selenium-bot.py”]
CMD ["/bin/bash"]
