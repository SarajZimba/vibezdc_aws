from django import forms
from django.forms.models import inlineformset_factory
from root.forms import BaseForm  # optional

from .models import ProductCategory, BudClass, TaxBracket, ProductPoints



class ProductCategoryForm(BaseForm, forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
        ]

class BudClassForm(BaseForm, forms.ModelForm):
    class Meta:
        model = BudClass
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
        ]

class TaxBracketForm(BaseForm, forms.ModelForm):
    class Meta:
        model = TaxBracket
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
        ]

class ProductPointsForm(BaseForm, forms.ModelForm):

    class Meta:
        model = ProductPoints
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
        ]
        widgets = {
            "product": forms.Select(
                attrs={
                    "class": "form-select",
                    "data-control": "select2",
                    "data-placeholder": "Select Product",
                }
            ),
        }


class ProductPointsUpdateForm(BaseForm, forms.ModelForm):

    class Meta:
        model = ProductPoints
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
            "product"
        ]



from .models import Product
from organization.models import Branch


# class ProductForm(BaseForm, forms.ModelForm):
#     branch = forms.ModelChoiceField(queryset=Branch.objects.all())
#     branch_quantity = forms.PositiveIntegerField()
#     class Meta:
#         model = Product
#         fields = "__all__"
#         exclude = [
#             "is_deleted",
#             "status",
#             "deleted_at",
#             "sorting_order",
#             "slug",
#             "is_featured",
#             "product_id",
#         ]
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["price"].label = "Selling Price"
#         self.fields["category"].label = "StrainType"
#         self.fields["description"].widget = forms.Textarea(attrs={"rows": 3, "class": "form-select"})
#         if self.instance.id:
#             # Show the 'reason' field when updating an existing product
#             self.fields["reason"].widget = forms.Textarea(attrs={"rows": 3, "class": "form-select"})
#         else:
#             # Exclude the 'reason' field when creating a new product
#             del self.fields["reason"]

        # self.fields["debit_account"].widget.attrs = {
        #     "tags":"true",
        #     "class":"form-select",
        #     "data-control": "select2",
        #     "data-placeholder": "Select Account",
        # }

class ProductForm(BaseForm, forms.ModelForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)
    branch_quantity = forms.IntegerField(required=False)

    class Meta:
        model = Product
        fields = "__all__"
        exclude = [
            "thumbnail",
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
            "product_id",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["price"].label = "Selling Price"
        self.fields["category"].label = "StrainType"
        self.fields["description"].widget = forms.Textarea(attrs={"rows": 3, "class": "form-select"})

        if self.instance.id:
            # Show the 'reason' field when updating an existing product
            self.fields["reason"].widget = forms.Textarea(attrs={"rows": 3, "class": "form-select"})
        else:
            # Exclude the 'reason' field when creating a new product
            del self.fields["reason"]

    def clean(self):
        cleaned_data = super().clean()

        is_taxable = cleaned_data.get('is_taxable')
        taxbracket = cleaned_data.get('taxbracket')

        if is_taxable == True:
            if taxbracket is None:
                raise forms.ValidationError("Taxable Products must have a taxbracket")

        return cleaned_data

    def save(self, commit=True):
        product = super().save(commit=commit)
        if self.cleaned_data.get('branch') and self.cleaned_data.get('branch_quantity'):

            branch = self.cleaned_data['branch']
            branch_quantity = self.cleaned_data['branch_quantity']

            branch_stock = BranchStock(product=product, branch=branch, quantity=branch_quantity)
            branch_stock.save()

        return product
        

from .models import CustomerProduct


class CustomerProductForm(BaseForm, forms.ModelForm):
    class Meta:
        model = CustomerProduct
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "slug",
            "is_featured",
            "agent",
        ]

from .models import ProductStock

class ProductStockForm(BaseForm, forms.ModelForm):
    class Meta:
        model = ProductStock
        fields = '__all__'
        exclude = [ 'sorting_order', 'is_featured', 'is_deleted', 'status', 'deleted_at',]

from .models import BranchStock
class BranchStockForm(BaseForm, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'] = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False))
        self.fields["product"].widget.attrs = {
            "class":"form-select",
            "data-control": "select2",
            "data-placeholder": "Select Item",
        }

    class Meta:
        model = BranchStock
        fields = '__all__'
        exclude = ['is_deleted', 'status', 'deleted_at','sorting_order', 'is_featured']