from django.urls import path
from .views import ProductListCreateView, ProductDetailView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]

# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MjYzNDY4NiwiaWF0IjoxNzcyNjE2Njg2LCJqdGkiOiIyYzEzY2E4NTU4OGU0NjJiOThjMzg0ODIxNDgxYzliNCIsInVzZXJfaWQiOiI1In0.4mnj0iK-Plh4Y0vBPl-lnMqJfoppgz-oc2hbCRutb7E",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcyNjE3NTg2LCJpYXQiOjE3NzI2MTY2ODYsImp0aSI6ImRkNTIzNjc0NzMxYjQxYTI4OTQ4NTg4MGYwYmQ1ZDA4IiwidXNlcl9pZCI6IjUifQ.mBpAHx-BMBwqf_WN2EBv2NPe-LbfzViPiX6Ut4r1Z3s"
# }

# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MjYzNDg4OSwiaWF0IjoxNzcyNjE2ODg5LCJqdGkiOiJlMjY4MDhkYmI5MGM0OGU0YjgyMmI1ZjVmMTA5OGIzZiIsInVzZXJfaWQiOiI2In0.fLxsYBvt2hBTf1Mn0mB5mhb-tDW3MTE5CwrIwN4ZP6k",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcyNjE3Nzg5LCJpYXQiOjE3NzI2MTY4ODksImp0aSI6ImMyMzE5NWMxZjI3MTQ0MWM4ZDE4MTUwNTNlM2YyNDZkIiwidXNlcl9pZCI6IjYifQ.EbHVC71j92A6ggRPd1HFpYXnPEhbKtfmZZfKa2onm_s"
# }