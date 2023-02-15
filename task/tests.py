######################################################################
# Copyright (c) 2023 Dmitry Pasichko. All rights reserved. #
######################################################################
from django.test import TestCase
from django.test import Client
from django.conf import settings

test_user_name = "admin"
teas_password = "000000"


def get_client():
    return Client()


def test_create_task_success():
    client = get_client()
    client.post({

    })


def test_create_task_failed():
    pass


def test_change_status_as_assignee():
    pass


def test_change_status_as_creator():
    pass


def test_add_comment_to_task():
    pass


def test_add_nested_task():
    pass
