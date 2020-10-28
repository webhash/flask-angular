FROM python:3.5
RUN pip install Flask==1.1.2 redis==3.5.3 flask_cors==3.0.9
RUN useradd -ms /bin/bash admin
USER admin
WORKDIR /app
COPY flask_app /app
EXPOSE 9999
CMD ["python" , "app.py"]