from django.contrib import admin


from .models import Product, Order, Cart, CartItem

admin.site.register(Product)
admin.site.register(Order)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = (CartItemInline,)
    list_display = ('id','cart_id','user')
    readonly_fields = ('cart_id', ) 

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id','cart', 'product', 'quantity')