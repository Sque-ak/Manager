from django.urls import path
from . import views
from .services.railwayorders import logic_order


urlpatterns = [
    path('', views.RailwayOrderView.as_view(), name = 'railway_order_page'),
    path('railway-order/create', views.NewRailwayOrder, name = 'railway_create'),
    path('railway-order/update/<int:pk>', views.RailwayOrderUpdateView.as_view(), name = 'railway_update_page'),

    path('railway-order-address/create', views.RailwayAddressCreatePopup, name = 'railway_address_create_page'),
    path('railway-order-address/<int:pk>/edit/', views.RailwayAddressEditPopup),
    path('railway-order-address/ajax/get_address_id', logic_order.get_address_id),
    
    path('railway-order-shipper/create', views.RailwayShipperCreatePopup, name = 'railway_shipper_create_page'),
    path('railway-order-shipper/<int:pk>/edit/', views.RailwayShipperEditPopup),
    path('railway-order-shipper/ajax/get_shipper_id', logic_order.get_shipper_id),

    path('railway-order-supplier/create', views.RailwaySupplierCreatePopup, name = 'railway_supplier_create_page'),

    path('railway-order/send-train/<int:pk>', views.SendTrain, name = 'railway_send_train'),
]
