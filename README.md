# postthis

A CMS to post to different social media platforms.

![Tests](https://github.com/spousesupportgroup/postthis/actions/workflows/ci.yml/badge.svg)
[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Übersetzungsstatus](https://hosted.weblate.org/widget/postthis/postthis/svg-badge.svg)](https://hosted.weblate.org/engage/postthis/)
[![Documentation Status](https://readthedocs.org/projects/postthis/badge/?version=latest)](https://postthis.readthedocs.io/en/latest/?badge=latest)
[![Maintainability](https://api.codeclimate.com/v1/badges/0e6d7b8c0672d1bbdc56/maintainability)](https://codeclimate.com/github/spousesupportgroup/postthis/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/0e6d7b8c0672d1bbdc56/test_coverage)](https://codeclimate.com/github/spousesupportgroup/postthis/test_coverage)


License: GPLv3

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    mypy postthis

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    coverage run -m pytest
    coverage html
    open htmlcov/index.html

#### Running tests with pytest

    pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd postthis
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd postthis
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd postthis
celery -A config.celery_app worker -B -l info
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [MailHog](https://github.com/mailhog/MailHog) with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

### Translation
We use weblate to translate our project.

<a href="https://hosted.weblate.org/engage/postthis/">
<img src="https://hosted.weblate.org/widget/postthis/postthis/multi-blue.svg" alt="Übersetzungsstatus" />
</a>
