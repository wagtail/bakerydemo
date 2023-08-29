import logging
from functools import partialmethod
from typing import Any

import django
from django import forms
from django.core.cache import cache
from django.db.models import NOT_PROVIDED, CharField, JSONField
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .exceptions import (
    DataverseConfigurationError,
    DataverseConnectionError,
    DataverseUserPermissionError,
)
from .utils import get_api_client

logger = logging.getLogger(__name__)


class DataverseMultipleChoiceField(forms.TypedMultipleChoiceField):
    widget = forms.CheckboxSelectMultiple


class DataverseChoiceFieldMixin:

    form_field_class = forms.TypedChoiceField

    def __init__(
        self,
        verbose_name: str,
        name: str,
        table_id: str = None,
        pk_column: str = None,
        label_column: str = None,
        **kwargs,
    ):
        self.table_id = table_id
        self.pk_column = pk_column
        self.label_column = label_column
        self._data_fetch_error = None
        if django.VERSION < (4, 2):
            kwargs.pop("db_comment", None)
            kwargs.pop("db_default", None)

        return super().__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        """
        Overrides Field.deconstruct() to include the required "table_id", "pk_column"
        and "label_column" values, and to prevent evaluation / inclusion of self.choices.
        """
        kwargs = {
            "table_id": self.table_id,
            "pk_column": self.pk_column,
            "label_column": self.label_column,
        }

        possibles = {
            "verbose_name": None,
            "primary_key": False,
            "max_length": None,
            "unique": False,
            "blank": False,
            "null": False,
            "db_index": False,
            "default": NOT_PROVIDED,
            "db_default": NOT_PROVIDED,
            "editable": True,
            "serialize": True,
            "help_text": "",
            "db_column": None,
            "db_comment": None,
            "db_tablespace": None,
            "auto_created": False,
            "validators": [],
            "error_messages": None,
        }
        if django.VERSION < (4, 2):
            possibles.pop("db_comment")
            possibles.pop("db_default")

        attr_overrides = {
            "unique": "_unique",
            "error_messages": "_error_messages",
            "validators": "_validators",
            "verbose_name": "_verbose_name",
            "db_tablespace": "_db_tablespace",
        }
        for name, default in possibles.items():
            value = getattr(self, attr_overrides.get(name, name))
            # Do correct kind of comparison
            if name == "validators":
                if value != default:
                    kwargs[name] = value
            else:
                if value is not default:
                    kwargs[name] = value

        # Work out path
        path = "%s.%s" % (self.__class__.__module__, self.__class__.__qualname__)

        # Return basic info - subclasses may override this
        return self.name, path, [], kwargs

    def _check_choices(self):
        # Prevent checking of self.choices
        return []

    def contribute_to_class(self, cls, name, private_only=False):
        """
        Overrides Field.contribute_to_class() to prevent evaluation
        of self.choices and to ALWAYS add the get_x_display() method
        to the model class.
        """
        self.set_attributes_from_name(name)
        self.model = cls
        cls._meta.add_field(self, private=private_only)
        if self.column:
            setattr(cls, self.attname, self.descriptor_class(self))

        if "get_%s_display" % self.name not in cls.__dict__:
            setattr(
                cls,
                "get_%s_display" % self.name,
                partialmethod(cls._get_FIELD_display, field=self),
            )

    @cached_property
    def api_client(self):
        return get_api_client()

    def get_choice_data(self):
        cache_key = "dataverse:{0}:choice_data".format(self.table_id)
        result = cache.get(cache_key, None)
        if result is None:
            result = self.api_client.get_rows(
                self.table_id,
                columns=[self.pk_column, self.label_column],
                order_by=self.label_column,
            )
            cache.add(cache_key, result, 60)
        return result

    @property
    def choices(self):
        self._data_fetch_error = None
        try:
            rows = self.get_choice_data()
        except (
            DataverseConfigurationError,
            DataverseConnectionError,
            DataverseUserPermissionError,
        ) as e:
            logger.error(
                f"Row data for table '{self.table_id}' could not be fetched from Dataverse. Using empty "
                f"choices for field '{self.name}' for now.",
                exc_info=e,
            )
            self.data_fetch_error = e
            return []
        else:
            return [(r[self.pk_column], r[self.label_column]) for r in rows]

    @choices.setter
    def choices(self, value):
        # Ignore attempts to set choices in Field.__init__()
        return None

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        if form_class is None:
            form_class = self.form_field_class
        if choices_form_class is None:
            choices_form_class = self.form_field_class
        return super().formfield(
            form_class=form_class, choices_form_class=choices_form_class, **kwargs
        )


class DataverseReferenceField(DataverseChoiceFieldMixin, CharField):
    non_db_attrs = getattr(CharField, "non_db_attrs", ()) + (
        "table_id",
        "pk_column",
        "label_column",
    )

    def __init__(
        self,
        verbose_name: str = None,
        name: str = None,
        # DataverseChoiceFieldMixin specific
        table_id: str = None,
        pk_column: str = None,
        label_column: str = None,
        # Automatically created ID columns in Dataverse use GUIDs, so we can
        # set a reasonable max_length by default
        max_length: int = 36,
        # Other BaseField args we want to support
        primary_key: bool = False,
        unique: bool = False,
        blank: bool = False,
        null: bool = False,
        db_index: bool = False,
        default: Any = NOT_PROVIDED,
        editable: bool = True,
        serialize: bool = True,
        help_text: str = "",
        db_column: str = None,
        db_tablespace: str = None,
        auto_created: bool = False,
        error_messages: dict = None,
        db_comment: str = None,
        db_default: Any = NOT_PROVIDED,
    ):
        return super().__init__(
            verbose_name,
            name,
            table_id,
            pk_column,
            label_column,
            max_length=max_length,
            primary_key=primary_key,
            unique=unique,
            blank=blank,
            null=null,
            db_index=db_index,
            default=default,
            editable=editable,
            serialize=serialize,
            help_text=help_text,
            db_column=db_column,
            db_tablespace=db_tablespace,
            auto_created=auto_created,
            error_messages=error_messages,
            db_comment=db_comment,
            db_default=db_default,
        )


class DataverseMultipleReferenceField(DataverseChoiceFieldMixin, JSONField):

    form_field_class = DataverseMultipleChoiceField
    default_error_messages = {
        "invalid": _("'%(value)s' value must be a list of strings."),
    }
    non_db_attrs = getattr(JSONField, "non_db_attrs", ()) + (
        "table_id",
        "pk_column",
        "label_column",
    )

    def __init__(
        self,
        verbose_name: str = None,
        name=None,
        # DataverseChoiceFieldMixin specific
        table_id: str = None,
        pk_column: str = None,
        label_column: str = None,
        # Other BaseField args we want to support
        blank: bool = False,
        null: bool = False,
        db_index: bool = False,
        default: Any = NOT_PROVIDED,
        editable: bool = True,
        serialize: bool = True,
        help_text: str = "",
        db_column: str = None,
        db_tablespace: str = None,
        auto_created: bool = False,
        error_messages: dict = None,
        db_comment: str = None,
        db_default: str = NOT_PROVIDED,
    ):
        super().__init__(
            verbose_name,
            name,
            table_id,
            pk_column,
            label_column,
            blank=blank,
            null=null,
            db_index=db_index,
            default=list if default is NOT_PROVIDED else default,
            editable=editable,
            serialize=serialize,
            help_text=help_text,
            db_column=db_column,
            db_tablespace=db_tablespace,
            auto_created=auto_created,
            error_messages=error_messages,
            db_comment=db_comment,
            db_default=db_default,
        )

    def validate(self, value, model_instance):
        if isinstance(value, (list, tuple)):
            # Validate each value individually
            for value in value:
                super().validate(value, model_instance)
        super(JSONField, self).validate(value, model_instance)

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        if form_class is None:
            form_class = self.form_field_class
        if choices_form_class is None:
            choices_form_class = self.form_field_class
        return super(JSONField, self).formfield(
            form_class=form_class, choices_form_class=choices_form_class, **kwargs
        )
