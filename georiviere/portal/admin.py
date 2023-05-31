from admin_ordering.admin import OrderableAdmin
from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from leaflet.admin import LeafletGeoAdmin

from georiviere.portal.models import MapBaseLayer, MapGroupLayer, MapLayer, Portal


class MapLayerAdminTabularForm(forms.ModelForm):
    class Meta:
        model = MapLayer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group_layer'].widget.can_add_related = False
        self.fields['group_layer'].widget.can_delete_related = False
        self.fields['group_layer'].widget.can_change_related = False

        if self.instance.pk:
            self.fields['group_layer'].queryset = self.fields['group_layer'].queryset.filter(
                portal=self.instance.portal)


class MapLayerAdminTabularInline(OrderableAdmin, admin.TabularInline):
    classes = ('collapse',)
    verbose_name = _('Map layer')
    verbose_name_plural = _('Map layers')
    model = MapLayer
    extra = 0
    form = MapLayerAdminTabularForm
    ordering_field = "order"
    ordering = ('-group_layer', )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class MapGroupLayerAdminTabularInline(OrderableAdmin, admin.TabularInline):
    classes = ('collapse',)
    verbose_name = _('Map group layer')
    verbose_name_plural = _('Map groups layer')
    model = MapGroupLayer
    extra = 0
    ordering_field = "order"


class MapBaseLayerAdminTabularInline(OrderableAdmin, admin.TabularInline):
    classes = ('collapse',)
    verbose_name = _('Map base layer')
    verbose_name_plural = _('Map base layers')
    model = MapBaseLayer
    extra = 0
    ordering_field = "order"


class PortalAdmin(LeafletGeoAdmin, OrderableAdmin, admin.ModelAdmin):
    list_display = ('name', 'website', 'title')
    search_fields = ('name', 'website')
    inlines = [MapBaseLayerAdminTabularInline, MapGroupLayerAdminTabularInline, MapLayerAdminTabularInline]

    def get_inline_instances(self, request, obj=None):
        return obj and super().get_inline_instances(request, obj) or []


class MapBaseLayerAdmin(OrderableAdmin, admin.ModelAdmin):
    ordering_field = "order"
    list_editable = ["order"]
    list_display = ('label', 'url', 'order')
    search_fields = ('label', )


class MapGroupLayerAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['portal'].disabled = True
        self.fields['portal'].widget.can_add_related = False
        self.fields['portal'].widget.can_delete_related = False
        self.fields['portal'].widget.can_change_related = False


class MapGroupLayerAdmin(OrderableAdmin, admin.ModelAdmin):
    ordering_field = "order"
    list_editable = ["order"]
    list_display = ('portal', 'label', 'order')
    search_fields = ('label',)
    ordering = ('-portal',)
    form = MapGroupLayerAdminForm


class MapLayerAdminForm(forms.ModelForm):
    class Meta:
        model = MapLayer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group_layer'].widget.can_add_related = False
        self.fields['portal'].disabled = True
        self.fields['portal'].widget.can_add_related = False
        self.fields['portal'].widget.can_delete_related = False
        self.fields['portal'].widget.can_change_related = False
        self.fields['group_layer'].widget.can_delete_related = False
        self.fields['group_layer'].widget.can_change_related = False
        self.fields['group_layer'].queryset = MapGroupLayer.objects.filter(portal=self.instance.portal)


class MapLayerAdmin(OrderableAdmin, admin.ModelAdmin):
    ordering_field = "order"
    list_editable = ["order"]
    list_display = ('portal', 'group_layer', 'label', 'layer_type', 'order')
    search_fields = ('label',)
    ordering = ('-portal', '-group_layer',)
    form = MapLayerAdminForm

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Portal, PortalAdmin)
admin.site.register(MapBaseLayer, MapBaseLayerAdmin)
admin.site.register(MapGroupLayer, MapGroupLayerAdmin)
admin.site.register(MapLayer, MapLayerAdmin)
