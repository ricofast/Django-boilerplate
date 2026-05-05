from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .forms import ItemForm
from .models import Item


class OwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or obj.owner == self.request.user


class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'core/item_list.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Item.objects.all()
        return Item.objects.filter(owner=self.request.user)


class ItemDetailView(LoginRequiredMixin, OwnerOrAdminMixin, DetailView):
    model = Item
    template_name = 'core/item_detail.html'


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'core/item_form.html'
    success_url = reverse_lazy('core:item-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, OwnerOrAdminMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'core/item_form.html'
    success_url = reverse_lazy('core:item-list')


class ItemDeleteView(LoginRequiredMixin, OwnerOrAdminMixin, DeleteView):
    model = Item
    template_name = 'core/item_confirm_delete.html'
    success_url = reverse_lazy('core:item-list')
