from django.shortcuts import render,get_object_or_404,redirect
from django.core.validators import ValidationError
from django.db.models import Q
from django.contrib import messages



#============== import from current app ================
from .models import Product,ProductType,Orders
from .forms import ProductForm,ProductTypeForm
from . import orders,total


# Create your views here.
# =================== display all products in the shop ==========================
def index_page(request):
    product_type = Product.objects.order_by('expire_date').all()
    # product = product_type.producttype_set.all()
    context={"products":product_type}
    return render(request,'Seller/index.html',context)

# ==================== search product in the shop ==================
def search_product(request):
    """ user enters the name of the product to search"""

    item_property = request.POST['search']
    #search here
    products = Product.objects.filter(
                                        Q(product_name__icontains=item_property)|
                                        Q(price__icontains=item_property)|
                                        Q(product_type__type_name__icontains=item_property)
                                    ).order_by("-expire_date").all()
    context = {
        "products":products,
        "item":item_property,
        }
    return render(request,"Seller/search_results.html",context)

# ====================== add product to database =====================
def add_to_stock(request):
    """ add product type and the product to stock"""
    product_Type = ProductType.objects.all()
    # current_trip = Trip.objects.filter("-date_added").all()
    # context = {"trip":current_trip,}
    if request.method == "POST":
        # user has restock the shop
        form = ProductForm(request.POST)

        product_name = request.POST['productName']
        product_price = request.POST['price']
        productsnumber = request.POST["numberofproducts"]
        mandate = request.POST['manuf_date']
        expiredate = request.POST['expire_date']
        filesimage=request.FILES['product_image']
        product_description = request.POST["description"]
        productform = Product(product_name=product_name,price=product_price,
                                number_of_products=productsnumber,manuf_date=mandate,
                                expire_date=expiredate,image=filesimage,description=product_description)
        # return form with data
        try:
            if form.is_valid():
                product = form.save(commit=False)
                productform.product_type = product.product_type
                productform.save()
                # valid data has been provided
                return redirect("seller:home")
        except ValidationError:
            pass
    else:
        form = ProductForm()
    context = {
        "items":product_Type,
        "form":form,
        # "trip":current_trip,
    }
    
    return render(request,"Seller/add_product.html",context)

# ================== store product buy category ================
def add_category(request):
    """add catergoty of products sell by shop"""
    if request.method == "POST":
        # post the data
        form = ProductTypeForm(data=request.POST)
        # validate the data
        if form.is_valid():
            form.save()
            # go add add the products
            return redirect("seller:expenses")
    else:
        # render empty form
        form = ProductTypeForm()
    context = {
        "form":form
    }
    return render(request,"Seller/add_category.html",context)

#  ============================ set expenses during buying of produts===================
def set_expenses(request):
    """add expenses that took in buying the products"""
    
    if request.method == "POST":
        # name = request.POST["TripName"]
        # amount= request.POST["amount"]
        # other = request.POST["others"]
        # trip = Trip(trip_name=name,purchases_total=amount,other_charges=other)
        # trip.save() 
        return redirect("seller:category")
    
    return render(request,"Seller/expense.html")

# ======================== profile of the seller ======================
def profile(request):
    """ User profile informations"""
    myProducts = Product.objects.all()
    context = {
        "products":myProducts,
    }
    return render(request,"Seller/profile.html",context)

# ========================delete product from database===========================
def delete_product(request,item_id):
    """delete the product from database"""
    product_to_remove = get_object_or_404(Product,pk=item_id)
    product_to_remove.delete()
    return redirect("seller:profile")

# ====================== edit product information ========================
def edit_product_info(request,product_id):
    """ edit the mistakes of the product information"""
    product = get_object_or_404(Product,pk=product_id)
    if request.method == "POST":
        edited_product_name = request.POST['productName']
        edited_product_price = request.POST['price']
        edited_productsnumber = request.POST["numberofproducts"]
        edited_mandate = request.POST['manuf_date']
        edited_expiredate = request.POST['expire_date']
        edited_filesimage=request.FILES['product_image']
        edited_product_description = request.POST["description"]
        productform = Product(
            product_name=edited_product_name,price=edited_product_price,
            number_of_products=edited_productsnumber,manuf_date=edited_mandate,
            expire_date=edited_expiredate,image=edited_filesimage,description=edited_product_description
            )
        productform.product_type = product.product_type
        productform.save()
        return redirect("seller:profile")
    context={
        "product":product,
    }
    return render(request,'Seller/edit_product_info.html',context)

# ============================== show product description =======================================
def show_product_description(request,productId):
    """ show the detailed description of the product"""
    product_description = get_object_or_404(Product,pk=productId)
    context={
        "product":product_description,
    }
    return render(request,'Seller/show_description.html',context)

# ================== add to cart =====================================
def add_to_cart(request,product_id):
    """add product to cart"""
    product = get_object_or_404(Product,pk=product_id)
    if request.method == "POST":
        number = int(request.POST["number_to_buy"])
        # add the item to
        current_number = product.number_of_products
        if current_number < number:
            messages.error(request,f"{current_number} is less than {number}. Enter a less or equal number")
        else:
            if number>=1:

                name = product.product_name
                price = float(product.price)
                total['total_price'] += price* number
                orders.append({"product":name,"number":number,
                    "price":price,"id":product.id
                })
                return redirect("seller:home")
            messages.warning(request,"Invalid Input")
    context = {
        "product":product,
    }
    return render(request,'Seller/orders.html',context)
        
# ================================ my order to buy ===============================
def myOrders(request):
    """ buy bulk items"""
    " get the product to buy and the bought product"""
    # get the product by its id
    if request.method == "POST":
        # the customer bought the product
        customer_name = request.POST["customer_name"]
        customer_email = request.POST["customer_email"]
        if len(orders) > 0:
            buy_ordered_products(request)
            messages.success(request, customer_name+" "+ customer_email +" Thanks For Buying From Us. See You Next Time.")
            clear_orders(request)
            return redirect("seller:my-orders")
        else:
            messages.error(request,"Orders Must Not Be Empty")
    context = {
        "orders_number":orders.__len__(),
        "orders":orders,
        "total":total,

    }
    return render(request,'Seller/myOrders.html',context)

# ============================= buy ordered products ==============================
def buy_ordered_products(request):
    """ process all items to buy"""
    for item in orders:
        boughts = item["number"]
        product_id = item["id"]
        product_bought = get_object_or_404(Product,pk=product_id)
        # remove the number of products bought from the stock
        # at the time of buying if orders is greater than number to buy 
        at_buy_number = product_bought.number_of_products
        if at_buy_number >= int(boughts):
            try:
                product_bought.number_of_products -= int(boughts)
                # save the remaining to the stock
                product_bought.save()
            except ValueError:
                pass
        else:
            messages.error(request,"Your Resquests Are More Than Stock Products")

# ============================== clear orders============================
def clear_orders(request):
    """ clear orders"""
    total['total_price'] = 0.0
    orders.clear()
    return redirect("seller:my-orders")