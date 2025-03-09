import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Brand, Category, Product

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'description', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['is_active']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'description', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['is_active']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'category', 'price', 'stock', 'is_active', 'description', 'created_at', 'updated_at']
    search_fields = ['title', 'brand__name', 'category__name']
    list_filter = ['is_active', 'brand', 'category']
    list_editable = ('stock',)

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj)) # Convertendo para lista
        if not obj:  # Adiciona 'stock' apenas no formulário de criação
            fields.append('stock') # Usando append para adicionar à lista
        return fields

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        writer = csv.writer(response)
        writer.writerow(['titulo', 'marca', 'categoria', 'preço', 'estoque', 'ativo', 'descrição', 'criado em', 'atualizado em'])
        for product in queryset:
            writer.writerow([product.title, product.brand.name, product.category.name, product.price, product.stock, product.is_active, product.description, product.created_at, product.updated_at])
        return response
    export_to_csv.short_description = 'Exportar para CSV'
    actions = ['export_to_csv']