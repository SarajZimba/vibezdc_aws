from .user import urlpatterns as user_urlpatterns
from .product import urlpatterns as product_urlpatterns
from .bill import urlpatterns as bill_urlpatterns
from .organization import urlpatterns as org_urlpatterns
from .discount_urls import urlpatterns as discount_urlspatterns
from .purchaserequisition_api import urlpatterns as purchaserequisition_urlpattern
from .accounting_urls import urlpatterns as accounting_urlpatterns
from .get_product import urlpatterns as get_product_urlpatterns
from .search import urlpatterns as search_url_patterns
from .bill_reprint import urlpatterns as bill_reprint_url_patterns
from .give_all_bills import urlpatterns as give_all_bills_url_patterns
from .product_list import urlpatterns as product_list_url_patterns
from .update_barcode import urlpatterns as update_barcode_url_patterns
from .clear_barcode import urlpatterns as clear_barcode_url_patterns
from .give_product_points import urlpatterns as give_product_points_patterns
from .delivery import urlpatterns as delivery_patterns
from .get_product_menu import urlpatterns as get_product_menu_urlpatterns
from .bill_todayid import urlpatterns as bill_todayid_urlpatterns
from .customer import urlpatterns as customer_history_urlpatterns



urlpatterns = (
    [] + user_urlpatterns + product_urlpatterns + bill_urlpatterns + org_urlpatterns+discount_urlspatterns+purchaserequisition_urlpattern+accounting_urlpatterns + get_product_urlpatterns + search_url_patterns + bill_reprint_url_patterns + give_all_bills_url_patterns + product_list_url_patterns + update_barcode_url_patterns + clear_barcode_url_patterns + give_product_points_patterns + delivery_patterns + get_product_menu_urlpatterns+ bill_todayid_urlpatterns + customer_history_urlpatterns
)
