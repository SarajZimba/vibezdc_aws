
from django.urls import path
urlpatterns = []

from .views import ChangeProductTax, ProductCategoryList,ProductCategoryDetail,ProductCategoryCreate,ProductCategoryUpdate,ProductCategoryDelete, BudClassList, BudClassCreate, BudClassDelete, BudClassDetail, BudClassUpdate, TaxBracketList, TaxBracketDelete,TaxBracketCreate, TaxBracketDetail, TaxBracketUpdate, ProductPointsCreate, ProductPointsDelete, ProductPointsDetail, ProductPointsUpdate,ProductPointsList


urlpatterns += [
path('prdct/category/', ProductCategoryList.as_view(), name='product_category_list'),
path('prdct/budclass/', BudClassList.as_view(), name='product_bud_list'),
path('prdct/taxbracket/', TaxBracketList.as_view(), name='product_taxbracket_list'),
path('prdct/points/', ProductPointsList.as_view(), name='product_points_list'),
path('prdct/category/<int:pk>/', ProductCategoryDetail.as_view(), name='product_category_detail'),
path('prdct/category/create/', ProductCategoryCreate.as_view(), name='product_category_create'),
path('prdct/category/<int:pk>/update/', ProductCategoryUpdate.as_view(), name='product_category_update'),
path('prdct/category/delete', ProductCategoryDelete.as_view(), name='product_category_delete'),
path('prdct/points/<int:pk>/', ProductPointsDetail.as_view(), name='product_points_detail'),
path('prdct/points/create/', ProductPointsCreate.as_view(), name='product_points_create'),
path('prdct/points/<int:pk>/update/', ProductPointsUpdate.as_view(), name='product_points_update'),
path('prdct/points/delete', ProductPointsDelete.as_view(), name='product_points_delete'),
path('prdct/bud/<int:pk>/', BudClassDetail.as_view(), name='product_bud_detail'),
path('prdct/bud/create/', BudClassCreate.as_view(), name='product_bud_create'),
path('prdct/bud/<int:pk>/update/', BudClassUpdate.as_view(), name='product_bud_update'),
path('prdct/bud/delete', BudClassDelete.as_view(), name='product_bud_delete'),
path('prdct/taxbracket/<int:pk>/', TaxBracketDetail.as_view(), name='tax_bracket_detail'),
path('prdct/taxbracket/create/', TaxBracketCreate.as_view(), name='tax_bracket_create'),
path('prdct/taxbracket/<int:pk>/update/', TaxBracketUpdate.as_view(), name='tax_bracket_update'),
path('prdct/taxbracket/delete', TaxBracketDelete.as_view(), name='tax_bracket_delete'),
path('prdct/change_product_tax/<int:pk>', ChangeProductTax.as_view(), name='change_product_tax'),
]
               
from .views import ProductList,ProductDetail,ProductCreate,ProductUpdate,ProductDelete, ProductUpload
urlpatterns += [
path('product/', ProductList.as_view(), name='product_list'),
path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
path('product/create/', ProductCreate.as_view(), name='product_create'),
path('product/<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
path('product/delete', ProductDelete.as_view(), name='product_delete'),
path('product/upload/', ProductUpload.as_view(), name='product_upload'),

]
               
from .views import CustomerProductList,CustomerProductDetail,CustomerProductCreate,CustomerProductUpdate,CustomerProductDelete
urlpatterns += [
path('prdct/client/', CustomerProductList.as_view(), name='customerproduct_list'),
path('prdct/client/<int:pk>/', CustomerProductDetail.as_view(), name='customerproduct_detail'),
path('prdct/client/create/', CustomerProductCreate.as_view(), name='customerproduct_create'),
path('prdct/client/<int:pk>/update/', CustomerProductUpdate.as_view(), name='customerproduct_update'),
path('prdct/client/delete', CustomerProductDelete.as_view(), name='customerproduct_delete'),
]

               
from .views import ProductStockList,ProductStockDetail,ProductStockCreate,ProductStockUpdate,ProductStockDelete, ProductThumbnail
urlpatterns += [
path('stock/', ProductStockList.as_view(), name='productstock_list'),
path('stock/<int:pk>/', ProductStockDetail.as_view(), name='productstock_detail'),
path('stock/create/', ProductStockCreate.as_view(), name='productstock_create'),
path('stock/<int:pk>/update/', ProductStockUpdate.as_view(), name='productstock_update'),
path('stock/delete', ProductStockDelete.as_view(), name='productstock_delete'),
path('thumbnail/save', ProductThumbnail.as_view(), name='product_save_for_thumbanail'),
]

from .views import BranchStockList,BranchStockDetail,BranchStockCreate,BranchStockUpdate,BranchStockDelete, ReconcileView, BranchStockUploadView, UpdateDateForReconcilationView, BranchstockUpload, BranchStockTotalList, BranchStockDeleteAll, export_branch_stock
urlpatterns += [
path('bstck/', BranchStockList.as_view(), name='branchstock_list'),
path('bstcktotal/', BranchStockTotalList.as_view(), name='branchstock_total'),
path('export_branch_stock/', export_branch_stock, name='export_branch_stock'),
path('bstck/<int:pk>/', BranchStockDetail.as_view(), name='branchstock_detail'),
path('bstck/create/', BranchStockCreate.as_view(), name='branchstock_create'),
path('bstck/<int:pk>/update/', BranchStockUpdate.as_view(), name='branchstock_update'),
path('bstck/delete', BranchStockDelete.as_view(), name='branchstock_delete'),
path('reconcile/', ReconcileView.as_view(), name='reconcile'),
path('bstck/upload-opening/', BranchStockUploadView.as_view(), name='branchstock_upload_opening'),
path('update-date-reconcilation/', UpdateDateForReconcilationView.as_view(), name='update_date_reconcilation'),
path('branchstock/upload/', BranchstockUpload.as_view(), name='branchstock_upload'),
path('branchstock/delete-all/', BranchStockDeleteAll.as_view(), name='delete_all_branchstock'), 



]
   