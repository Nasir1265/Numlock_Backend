from django.urls import path
from . import views
urlpatterns = [
   path("ping",views.ping,name="pings"),
   path('product/',views.Product_List.as_view()),
   path('create_product/',views.ProductCreateView.as_view()),
   path('best_seller/',views.Best_Seller.as_view()),
   path('latest_items/',views.Latest_Item.as_view()),
   path('book-service/', views.Brand_service.as_view(), name='book-service'),
   path('contact-form/', views.Contact_form.as_view(), name='contact-form'),

]
 