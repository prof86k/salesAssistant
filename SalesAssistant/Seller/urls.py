from django.urls import path
import random
import string


# ========== import form current app =========
from . import views as main_views

# ================ set app's name =============
app_name = "seller"
def random_generator():
    return random.choices(string.ascii_uppercase[:10])


call_it = random_generator()
# ================ config urls with views ===========================
urlpatterns = [
    # ================= url patterns ================================
    # home
    path('',main_views.index_page,name="home"),
    # add to stock

    path('add-to-stock/',main_views.add_to_stock,name="add-to-stock"),
    path('add/category/',main_views.add_category,name='category'),
    path('expenses',main_views.set_expenses,name="expenses"),
    # profile

    path('profile/',main_views.profile,name="profile"),
    path('product/editor/<int:product_id>/edit',main_views.edit_product_info,name="edit_product"),
    path('delete/item-number/<int:item_id>-from/database',main_views.delete_product,name="delete-item"),
    
    # orders
    path('my/order/',main_views.myOrders,name="my-orders"),
    path('clear/my/orders',main_views.clear_orders,name="clear-orders"),
    path('add/<int:product_id>to/cart',main_views.add_to_cart,name="add-to-cart"),
    
    # search
    path('searched/results/',main_views.search_product,name='search-results'),
    path('show/<int:productId>/detailed-description/',main_views.show_product_description,name='show-description'),
]
