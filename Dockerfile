FROM python:alpine3.17


WORKDIR /cloud_native_course_ex3
COPY main.py .
RUN pip install flask
RUN pip install flask_restful
RUN pip install requests
RUN pip install jsonify
RUN pip install make_response
RUN pip install OrderedDict
EXPOSE 8000
ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=8000
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
