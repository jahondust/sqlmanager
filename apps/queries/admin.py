from django.contrib import admin

from apps.queries.models import Category, Database, Query, Param


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'slug', ]
    list_display_links = ['name']
    search_fields = ('name',)


class DatabaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', ]
    list_display_links = ['name']
    search_fields = ('name',)


class ParamAdminInline(admin.TabularInline):
    model = Param


class QueryAdmin(admin.ModelAdmin):
    inlines = (ParamAdminInline, )
    list_display = ['title', 'description', 'slug', ]
    list_display_links = ['title']
    search_fields = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Database, DatabaseAdmin)
admin.site.register(Query, QueryAdmin)
