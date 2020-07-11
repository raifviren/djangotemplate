"""
Created at 11/07/20
@author: virenderkumarbhargav
"""
"""
Tests for the core/models.py
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.utils import DataError
from django.test import TestCase
from django.utils import timezone

from community.models import User


class UserTestCase(TestCase): # pylint: disable=too-many-public-methods
    """
    Test cases for creating User model objects
    """

    def setUp(self):
        """
        Make test database ready to run each test
        """
        User.objects.all().delete()

    def test_valid_data(self):
        """
        User with valid data
        """
        user = User(first_name='test',
                    last_name='user',
                    phone='+919999999999',
                    facebook_id='fb001',
                    email='abc@grappus.com',
                    age=20
                    )
        user.save()
        self.assertNotEqual(None, user)
        self.assertIsInstance(user, User)
        self.assertEqual('test', user.first_name)
        self.assertEqual('user', user.last_name)
        self.assertEqual('+919999999999', user.phone)
        self.assertEqual('fb001', user.facebook_id)
        self.assertEqual('abc@grappus.com', user.email)
        self.assertEqual(20, user.age)


    def test_first_name_too_long(self):
        """
        The first_name field was too long
        """
        msg = 'value too long for type character varying(30)'
        with self.assertRaisesMessage(DataError, msg):
            user = User(first_name='test' * 20,
                        last_name='user',
                        phone='+919999999999',
                        facebook_id='fb001',
                        email='abc@grappus.com',
                        age=20
                        )
            user.save()
            self.fail("'test_name_too_long' did not get the expected error")

    def test_last_name_too_long(self):
        """
        The executable_file field was too long
        """
        msg = 'value too long for type character varying(30)'
        with self.assertRaisesMessage(DataError, msg):
            user = User(first_name='test',
                        last_name='user' * 20,
                        phone='+919999999999',
                        facebook_id='fb001',
                        email='abc@grappus.com',
                        age=20
                        )
            user.save()
            self.fail("'test_last_name_too_long' did not get the expected error")

    def test_phone_too_long(self):
        """
        The phone field was too long
        """
        msg = 'value too long for type character varying(16)'
        with self.assertRaisesMessage(DataError, msg):
            user = User(first_name='test',
                        last_name='user',
                        phone='+919999999999' * 2,
                        facebook_id='fb001',
                        email='abc@grappus.com',
                        age=20
                        )
            user.save()
            self.fail("'test_phone_too_long' did not get the expected error")

    def test_fb_id_too_long(self):
        """
        The fb_id field was too long
        """
        msg = 'value too long for type character varying(100)'
        with self.assertRaisesMessage(DataError, msg):
            user = User(first_name='test',
                        last_name='user',
                        phone='+919999999999',
                        facebook_id='f' * 101,
                        email='abc@grappus.com',
                        age=20
                        )
            user.save()
            self.fail("'test_fb_id_too_long' did not get the expected error")

    def test_google_id_too_long(self):
        """
        The google_id field was too long
        """
        msg = 'value too long for type character varying(100)'
        with self.assertRaisesMessage(DataError, msg):
            user = User(first_name='test',
                        last_name='user',
                        phone='+919999999999',
                        google_id='f' * 101,
                        email='abc@grappus.com',
                        age=20
                        )
            user.save()
            self.fail("'test_google_id_too_long' did not get the expected error")

    def test_email_too_long(self):
        """
        The archive_location field was too long
        """
        msg = 'value too long for type character varying(254)'
        with self.assertRaisesMessage(DataError, msg):
            user = User(first_name='test',
                        last_name='user',
                        phone='+919999999999',
                        facebook_id='fb001',
                        email='abc@grappus.com'*256,
                        age=20
                        )
            user.save()
            self.fail("'test_archive_location_too_long' did not get the expected error")

    def test_invalid_age(self):
        """
        The size field was not provided
        """
        user = User(first_name='test',
                    last_name='user',
                    phone='+919999999999',
                    facebook_id='fb001',
                    email='abc@grappus.com',
                    age='20'
                    )
        user.save()
        print(user)


    def test_defaults(self):
        """
        Do not provide fields that can be defaulted and test their values
        """
        user = User(email='someone@email.com', password='somepasswd')
        user.save()
        self.assertNotEqual(None, user)
        self.assertIsInstance(user, User)

    def test_updated_at(self):
        """
        Check is updated_at changes after updating a object
        """
        user = User(first_name='test',
                    last_name='user',
                    phone='+919999999999',
                    facebook_id='fb001',
                    email='abc@grappus.com',
                    age='20'
                    )
        user.save()
        updated1 = user.updated_at
        user.first_name = 'Sumeet'
        user.save(update_fields=['first_name'])
        updated2 = user.updated_at
        result = updated2 > updated1
        self.assertTrue(result, True)
