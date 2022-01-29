# UploadFileService

### Upload file service API written in Django

- This API can be used to receive a file on any format and set it to two different AWS S3 Buckets
- Max file size: 5.0 Mb

#### Setup environment variables

Create `.env` file and copy the `.env_template` content. For example:

```
$ cp .env_template .env
```

#### Env vars:

```
- AWS_ACCESS_KEY_ID = 'your aws access key id'
- AWS_SECRET_ACCESS_KEY = 'your aws access key secret'
- S3_BUCKET_1 = 'first bucket name'
- S3_BUCKET_2 = 'second bucket name'
```

#### Setup:

```
pipenv install --dev
pipenv shell
```

#### Run App:
```
python main.py runserver
```

#### Run Tests
```
python manage.py test
```

#### Test on your machine:

```
curl -F file=@statement.pdf \
-F 'filename=statement.pdf' \
http://localhost:8000/upload
```