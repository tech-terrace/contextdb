from django.contrib import admin
from .models import Tag, Framework, Version, Variant, DocFile
from django.utils.html import format_html

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class FrameworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    filter_horizontal = ('tags',)

class VersionInline(admin.TabularInline):
    model = Version
    extra = 1

class FrameworkVersionAdmin(admin.ModelAdmin):
    inlines = [VersionInline]

class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1

class VersionAdmin(admin.ModelAdmin):
    list_display = ('framework', 'version_number', 'release_date')
    list_filter = ('framework',)
    search_fields = ('version_number',)
    inlines = [VariantInline]
    autocomplete_fields = ['framework']

class DocFileInline(admin.TabularInline):
    model = DocFile
    extra = 1

class VariantAdmin(admin.ModelAdmin):
    list_display = ('version', 'get_variant_type_display')
    list_filter = ('version__framework',)
    search_fields = ('version__version_number',)
    inlines = [DocFileInline]
    autocomplete_fields = ['version']

class DocFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'variant', 'token_count', 'file_link')
    list_filter = ('variant__version__framework',)
    search_fields = ('file_name',)
    autocomplete_fields = ['variant']

    def file_link(self, obj):
        if obj.get_file_url():
            return format_html("<a href='{url}' target='_blank'>{url}</a>", url=obj.get_file_url())
        return "-"
    file_link.short_description = "File URL"

# Register your models here.
admin.site.register(Tag, TagAdmin)
admin.site.register(Framework, FrameworkAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(DocFile, DocFileAdmin)