"""
Created at 11/07/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals, absolute_import

import uuid

import os

import pytz
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models, IntegrityError
from django.db.models import F
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator

from user.utils import upload_image_to
from user.constants import CONST_FILE_TYPE, CONST_LENGTH_MEDIA_TYPE
from user.utils.services import get_unique_slug


class BaseClass(models.Model):
    """ Base Class for all models

        id          ==> is chosen to be uuid field to ensure intra-model uniqueness
        is_deleted  ==> will used to mark an instance as deleted. We will
                        NEVER delete any instance from DB untill unless we have a
                        solid explanation for it
        created_at  ==> non-editable
        updated_at  ==> non-editable
    """
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True,
                          name="id", help_text="Unique ID")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    @property
    def created_at_ist(self):
        """Display each event time on the changelist in its own timezone"""
        fmt = '%B %d, %Y, %I:%M %p'
        dt = self.created_at.astimezone(pytz.timezone("Asia/Kolkata"))
        return dt.strftime(fmt)

    @property
    def updated_at_ist(self):
        """Display each event time on the changelist in its own timezone"""
        fmt = '%B %d, %Y, %I:%M %p'
        dt = self.updated_at.astimezone(pytz.timezone("Asia/Kolkata"))
        return dt.strftime(fmt)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        if hasattr(self, 'slug'):
            if not self.slug:
                if hasattr(self, 'title'):
                    self.slug = get_unique_slug(self, 'title', 'slug')
                if hasattr(self, 'name'):
                    self.slug = get_unique_slug(self, 'name', 'slug')
        return super(BaseClass, self).save(*args, **kwargs)

    class Meta(object):
        """ abstract=True because we do not want duplicate models """
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        try:
            if 'name' in self.__dict__.keys():
                return self.name
            elif 'text' in self.__dict__.keys():
                return self.text
            elif 'title' in self.__dict__.keys():
                return self.title
            elif 'first_name' or 'last_name' in self.__dict__.keys():
                if self.get_full_name != '':
                    return self.get_full_name
                elif self.username != '':
                    return self.username
                else:
                    return str('No Name')
            else:
                return str(self.id)
        except:
            return str(self.id)

    @classmethod
    def get_active_objects(cls, **kwargs):
        """
        @Summary: getting active objects in ordering wrt 'modified_at'
        :param kwargs:
        :return: query object
        """
        query = cls.objects.filter(is_deleted=False)  # pylint: disable=no-member
        if kwargs:
            query = query.filter(**kwargs)
        return query

    def get_similar_objects_by_category(self):
        """
        This will return all related objects based on category.
        """
        try:
            # if self.category:
            return self.__class__.get_active_objects(category=self.category)
            # else:
            #     raise IntegrityError('This %s is invalid.' % self.__class__.__name__)
        except KeyError:
            raise KeyError('%s object does not have any "category" attribute.' % self.__class__.__name__)

    def get_similar_objects_by_condition(self):
        """
        This will return all the Groups of the same Condition.
        """
        try:
            # if self.condition:
            return self.__class__.get_active_objects(condition=self.condition)
            # else:
            #     raise IntegrityError('This %s is invalid.' % self.__class__.__name__)
        except KeyError:
            raise KeyError('%s object does not have any "condition" attribute.' % self.__class__.__name__)

    def get_similar_objects_by_group(self):
        """
        This will return all the Groups of the same Condition.
        """
        try:
            # if self.support_group:
            return self.__class__.get_active_objects(support_group=self.support_group)
            # else:
            #     raise IntegrityError('This %s is invalid.' % self.__class__.__name__)
        except KeyError:
            raise KeyError('%s object does not have any "support_group" attribute.' % self.__class__.__name__)

    @classmethod
    def delete_object(cls, key):
        """
        @Summary: Deleting object for given id
        :param pk:
        :return: instance
        """
        obj = cls.objects.filter(id=key).first()  # pylint: disable=no-member
        if not obj:
            return False
        obj.is_deleted = True
        obj.save()

    @classmethod
    def get_by_ids(cls, ids, in_ids=True):
        """
        @Summary: Getting objects by id if there is single id or by list of ids
        :param ids:
        :param in_ids:
        :return: query object
        """
        if not isinstance(ids, list):
            ids = [ids, ]
        if in_ids:
            return cls.objects.filter(id__in=ids, is_deleted=False).order_by("created_at") # pylint: disable=no-member
        return cls.objects.filter(~models.Q(id__in=ids), models.Q(is_deleted=False)).order_by("created_at")  # pylint: disable=no-member, line-too-long


class BaseCreatedByModel(models.Model):
    """
    @Summary: This model can be used to add created_by field
    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)

    class Meta: # pylint: disable=old-style-class, too-few-public-methods , no-init
        """
        @Summary: Meta class to define meta properties
        """
        abstract = True


class BaseCommentModel(BaseClass, BaseCreatedByModel):
    """
    @Summary: Base model for comments
    """
    text = models.TextField(_('Comment'), blank=True, null=True)
    is_anonymous = models.BooleanField(default=False, help_text="If checked then owner detail must be hidden.")
    helpful = ArrayField(models.UUIDField(), default=[],
                         help_text="Id's of people who has marked this comment helpful.")

    class Meta: # pylint: disable=old-style-class, too-few-public-methods , no-init
        """
        @Summary: Meta class to define meta properties
        """
        abstract = True

    def mark_unmark_helpful(self, user_id):
        if self.helpful is None or user_id not in self.helpful:
            self.helpful.append(user_id)
            self.save()
            return True
        else:
            self.helpful.remove(user_id)
            self.save()
            return False


class BaseAttachmentModel(BaseCreatedByModel):
    """
    @Summary: Base model for attachments
    """
    file = models.FileField(upload_to=upload_image_to, blank=True)
    thumbnail = models.FileField(upload_to=upload_image_to,
                                 blank=True,
                                 validators=[FileExtensionValidator(
                                     allowed_extensions=['png', 'jpg', 'jpeg', 'gif']
                                 )])
    file_type = models.CharField(choices=CONST_FILE_TYPE, max_length=CONST_LENGTH_MEDIA_TYPE, blank=True)

    class Meta: # pylint: disable=old-style-class, too-few-public-methods , no-init
        """
        @Summary: Meta class to define meta properties
        """
        abstract = True
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """ On save, auto-fill file_type """
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        extension = os.path.splitext(self.file.name)[1][1:].lower()
        if extension in ['jpg', 'png', 'jpeg', 'gif']:
            self.file_type = 'image'
        elif extension in ['avi', 'mp4', 'mov', 'mpeg', 'flv', 'wmv', '3gp', 'm4v']:
            self.file_type = 'video'
        else:
            self.file_type = 'other'
        return super(BaseAttachmentModel, self).save(*args, **kwargs)


class BaseDisplayOrderClass(BaseClass):
    display_order = models.PositiveIntegerField(_('Display Order'), validators=[MinValueValidator(1)], blank=True, null=True,
                                                help_text="If left unchanged, order will be managed internally.")

    class Meta: # pylint: disable=old-style-class, too-few-public-methods , no-init
        """
        @Summary: Meta class to define meta properties
        """
        abstract = True
        ordering = ['display_order', '-created_at']

    def save(self, *args, **kwargs):
        self.update_order()
        return super(BaseDisplayOrderClass, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        queryset = self.get_order_queryset().order_by('display_order')
        queryset.filter(display_order__gt=self.display_order).update(display_order=F('display_order') - 1)
        super(BaseDisplayOrderClass, self).delete(*args, **kwargs)

    def update_order(self):
        queryset = self.get_order_queryset().order_by('display_order')
        if queryset.exists():
            max_limit = queryset.count()
        else:
            max_limit = 0
        if self._state.adding:
            if self.display_order is not None:
                if self.display_order >= max_limit + 1:
                    self.display_order = max_limit + 1
                    return
                queryset.filter(display_order__gte=self.display_order, display_order__lte=max_limit).update(
                    display_order=F('display_order') + 1)
                return
            self.display_order = max_limit + 1

        else:
            current_oder = self.__class__.objects.get(id=self.id).display_order
            if self.display_order != current_oder:
                if self.display_order >= max_limit + 1:
                    self.display_order = max_limit
                new_order = self.display_order
                if new_order > current_oder:
                    queryset.filter(display_order__gt=current_oder, display_order__lte=new_order).update(
                        display_order=F('display_order') - 1)
                elif new_order < current_oder:
                    queryset.filter(display_order__lt=current_oder, display_order__gte=new_order).update(
                        display_order=F('display_order') + 1)

