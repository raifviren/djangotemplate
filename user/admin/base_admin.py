"""
Created at 11/07/20
@author: virenderkumarbhargav
"""
import uuid

from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import unquote
from django.contrib.admin.widgets import AdminFileWidget
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.urls import reverse


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            if image_url:
                output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" width="100" height="100" \
                              style="object-fit: cover;"/></a> %s ' % \
                              (image_url, image_url, file_name, _('')))
            else:
                output.append(u'No Preview')
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class BaseAdminClass(admin.ModelAdmin):
    list_display_links = None
    readonly_fields = ('id', 'thumb_preview', 'created_at', 'updated_at', 'created_at_ist', 'updated_at_ist',
                       'created_by', 'view_attachment_tag')

    class Meta:
        abstract = True

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if request.user.is_superuser:
            obj.delete()
        else:
            obj.is_deleted = True
            obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(is_deleted=False)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.created_by = request.user
            instance.save()
        formset.save_m2m()

    def get_list_display(self, request):
        def manage(obj):
            """
            @summary: this fucntion provide two link Edit/Delete for list_display of models
            :param obj: current instance
            :return: two links to edit and delete using django admin reverse url for same
            """
            opts = self.model._meta
            opts.model_name = self.model._meta.model_name
            info = opts.app_label, opts.model_name
            preserved_filters = self.get_preserved_filters(request)
            change_url = add_preserved_filters({
                'preserved_filters': preserved_filters,
                'opts': opts
            }, reverse('admin:%s_%s_change' % info, args=[obj.id],))

            delete_url = add_preserved_filters({
                'preserved_filters': preserved_filters,
                'opts': opts
            }, reverse('admin:%s_%s_delete' % info, args=[obj.id],))

            return format_html(
                '<a class="changelink" href="{}">Edit</a>&nbsp;&nbsp;&nbsp;&nbsp;'
                '<a class="deletelink" href="{}">Delete</a>',
                change_url,
                delete_url
            )
        ls = list(self.list_display)
        if not request.user.is_superuser:
            ls.remove("is_deleted")
        return ls + [manage]

        #
        # return format_html(
        #     '<a class="changelink" href="{}">Edit</a>&nbsp;&nbsp;&nbsp;&nbsp;'
        #     '<a class="deletelink" href="{}">Delete</a>',
        #     reverse('admin:%s_%s_change' % info, args=[obj.id],),
        #     reverse('admin:%s_%s_delete' % info, args=[obj.id],)
        # )

    def thumb_preview(self, obj):
        """
        @summary:
        :param obj:
        :return:
        """
        if obj.image:
            return mark_safe('<img src="%s" style="width: 100px;" />' % obj.image.url)

        if obj.thumbnail:
            return mark_safe('<img src="%s" style="width: 100px;" />' % obj.thumbnail.url)
        else:
            return 'No Preview'

    thumb_preview.short_description = 'Preview'
    thumb_preview.allow_tags = True

    def view_attachment_tag(self, obj):
        if obj.attachments:
            head = '<h6 style="">Attachments</h6>'
            table = '<div>' \
                    '<table>' \
                    '<tbody>' \
                    '<tr>'
            for i in obj.attachments.all():
                table = table + "<td style='min-width: unset;'><a href='%s'><img height = 50px width=50px src='%s' /></a>" % (
                    i.file.url, i.file.url)
            table = table + '</tr>' \
                            '</tbody>' \
                            '</table>' \
                            '</div>'
            return mark_safe(_(head + table))
        else:
            head = '<h6 style=""> No Attachments</h4>'
            return mark_safe(_(head))

    view_attachment_tag.short_description = 'Preview'
    view_attachment_tag.allow_tags = True

    def custom_redirect_url(self, request):
        opts = self.model._meta
        preserved_filters = request.GET.urlencode()
        changelist_url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name))
        print(preserved_filters, opts)
        redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, changelist_url)
        return redirect_url

    def response_add(self, request, obj, post_url_continue=None):
        redirect_url = self.custom_redirect_url(request)
        if '_popup' or '_to_field' or '_continue' not in request.GET and redirect_url is not None:
            return HttpResponseRedirect(redirect_url)
        else:
            return super(BaseAdminClass, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        redirect_url = self.custom_redirect_url(request)
        if '_popup' or '_to_field' or '_continue' not in request.POST and redirect_url is not None:
            return HttpResponseRedirect(redirect_url)
            # return super(BaseAdminClass, self).change_view(request, obj, self.form, True)
        else:
            return super(BaseAdminClass, self).response_add(request, obj)


class BaseInline(object):
    extra = 0
    show_change_link = True

    def file_preview(self, obj):
        """
        @summary: this will return thumbnail preview for file field
        :param obj:
        :return:
        """
        if obj.file:
            image_url = obj.file.url
            return mark_safe(u' <a href="%s" target="_blank"><img src="%s" width="100" height="100" \
                             style="object-fit: cover;"/></a>' % \
                             (image_url, image_url))
        else:
            return 'No Preview'

    file_preview.short_description = 'File'
    file_preview.allow_tags = True

    def thumb_preview(self, obj):
        """
        @summary: this will return thumbnail preview for thumbnail field
        :param obj:
        :return:
        """
        if obj.thumbnail:
            image_url = obj.thumbnail.url
            return mark_safe(u' <a href="%s" target="_blank"><img src="%s" width="100" height="100" \
                             style="object-fit: cover;"/></a>' % \
                             (image_url, image_url))
        else:
            return 'No Preview'

    thumb_preview.short_description = 'Thumbnail'
    thumb_preview.allow_tags = True


class BaseTabularInline(BaseInline, admin.TabularInline):
    pass


class BaseStackedInline(BaseInline, admin.StackedInline):
    pass


class BaseAttachmentInline(BaseTabularInline):
    pass


def getTabularInline(getmodel, getform=None):
    """
    @summary: this function is a wrapper function that takes model and form as input and return tabular inline for same
    :param getmodel: required parameter to represent an inline
    :param getform: optional parameter to accept form to use for this inline
    :return: TabularInline for same
    """
    class GetTabularInline(BaseTabularInline):
        readonly_fields = ('created_at', 'updated_at', 'created_by', 'created_at_ist', 'updated_at_ist',)
        model = getmodel
        form = getform
        # fields = '__all__'
    return GetTabularInline