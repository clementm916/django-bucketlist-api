from django.contrib import admin

from .models import Bucketlist, Item


class ItemInline(admin.StackedInline):
    model = Item


class BucketlistAdmin(admin.ModelAdmin):
    inlines = [ItemInline, ]
    list_display = ('name', 'created_by', 'date_created', 'date_modified')
    list_filter = ('name', 'created_by', 'date_created', 'date_modified')
    search_fields = ('name',)


admin.site.register(Bucketlist, BucketlistAdmin)

# Register your models here.
