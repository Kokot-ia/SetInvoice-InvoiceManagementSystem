from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Item, Item_Category
from .forms import ItemForm, ItemCategoryForm

# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Item_Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Item_Category.objects.filter(user=self.request.user)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Item_Category
    form_class = ItemCategoryForm
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Item_Category
    form_class = ItemCategoryForm
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('category_list')
    pk_url_kwarg = 'category_id'

    def get_queryset(self):
        return Item_Category.objects.filter(user=self.request.user)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Item_Category
    template_name = 'inventory/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    pk_url_kwarg = 'category_id'

    def get_queryset(self):
        return Item_Category.objects.filter(user=self.request.user)

# Item Views
class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        queryset = Item.objects.filter(user=self.request.user).select_related('item_cat', 'user')
        
        # Get filter parameters
        category_id = self.request.GET.get('category')
        low_stock = self.request.GET.get('low_stock')
        search = self.request.GET.get('search')
        
        # Apply filters
        if category_id:
            queryset = queryset.filter(item_cat_id=category_id)
        
        if low_stock:
            queryset = queryset.filter(available_qty__lt=10)
        
        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(item_name__icontains=search) |
                Q(item_cat__item_cat_name__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Item_Category.objects.filter(user=self.request.user).order_by('item_cat_name')
        context['total_items'] = self.get_queryset().count()
        return context

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('item_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['item_cat'].queryset = Item_Category.objects.filter(user=self.request.user)
        return form

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('item_list')
    pk_url_kwarg = 'item_id'

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['item_cat'].queryset = Item_Category.objects.filter(user=self.request.user)
        return form

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'inventory/item_confirm_delete.html'
    success_url = reverse_lazy('item_list')
    pk_url_kwarg = 'item_id'

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)
