from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.index, name = 'index'),
    path('api/chart_data/', views.ChartAPIView.as_view()),
    path('orders/', views.OrdersListView.as_view(), name = 'orders'),

    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<str:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<str:pk>/print/', views.PrintOrderDetailView.as_view(), name='order_detail_print'),
    path('orders/<str:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('orders/<str:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),

    path('orders/<int:pk>/deletefield/', views.inOrderDeleteView.as_view(), name='in_order_delete'),
    path('orders/<int:pk>/updatefield/', views.inOrderUpdateView.as_view(), name='in_order_update'),
    path('orders/<str:pk>/createfield/', views.inOrderCreateView.as_view(), name='in_order_create'),
    path('orders/<str:pk>/sendorder/', views.inSendOrder, name='in_order_send'),

    path('orders/<str:pk>/alloworder/', views.allowOrder, name='allow_order'),
    path('orders/<str:pk>/disalloworder/', views.disallowOrder, name='disallow_order'),
    path('orders/<str:pk>/allowOrderManager/', views.allowOrderManager, name='allow_order_manager'),

    path('company/', views.companyListView.as_view(), name = 'company'),
    path('company/create/', views.companyCreateView.as_view(), name = 'company_create'),
    path('company/<int:pk>/update/', views.companyUpdateView.as_view(), name = 'company_update'),
    path('company/<int:pk>/delete/', views.companyDeleteView.as_view(), name = 'company_delete'),

    path('product/', views.productListView.as_view(), name = 'product'),
    path('product/create/', views.productCreateView.as_view(), name = 'product_create'),
    path('product/<int:pk>/update/', views.productUpdateView.as_view(), name = 'product_update'),
    path('product/<int:pk>/delete/', views.productDeleteView.as_view(), name = 'product_delete'),

    path('transport/', views.transportListView.as_view(), name = 'transport'),
    path('transport/create/', views.transportCreateView.as_view(), name = 'transport_create'),
    path('transport/<int:pk>/update/', views.transportUpdateView.as_view(), name = 'transport_update'),
    path('transport/<int:pk>/delete/', views.transportDeleteView.as_view(), name = 'transport_delete'),

    path('shipment/', views.shipmentListView.as_view(), name = 'shipment'),
    path('shipment/create/', views.shipmentCreateView.as_view(), name = 'shipment_create'),
    path('shipment/<int:pk>/update/', views.shipmentUpdateView.as_view(), name = 'shipment_update'),
    path('shipment/<int:pk>/delete/', views.shipmentDeleteView.as_view(), name = 'shipment_delete'),
]
