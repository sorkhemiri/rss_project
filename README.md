# RSS Management APP


```
ما در پیاله عکس رخ یار دیده‌ایم

ای بی‌خبر ز لذت شرب مدام ما
```
Technologies and databases:

`Python 3.8`

`FastAPI 0.68`

`Postgres 12`

`Redis 6`

## Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).


### Getting started

First, create a `.env` file and put it inside the root folder of the project.  
The `.env` file is the one that contains all your configurations, api keys, etc.
You can copy/paste the contents from `.env.example` to your `.env` file.  
then, run the command below:
```
docker-compose up --build -d
```
`Note:` if it's the **first time** to run the project, please execute the commands below to create the tables in the database.
```
$ cd path/to/project/directory
$ chmod +x generate_db.sh
$ ./generate_db.sh
```
`Note:` create and delete rss sources need admin permission so if register a user and run lines below to make it admin:
```
$ cd path/to/project/directory
$ chmod +x make_admin.sh
$ ./make_admin.sh username
```
for running the tests, run the command below:
```
$ cd path/to/project/directory
$ chmod +x run_test.sh
$ ./run_test.sh
```
**Note**: The first time you start your stack, it might take a few minutes for it to be ready. While the backend configures everything. You can check the logs to monitor it.

To check the logs, run:

```bash
docker-compose logs
```
### Contributing in this project

If you want to contribute in this project, make sure to read the [CONTRIBUTING.md](CONTRIBUTING.md) first.
