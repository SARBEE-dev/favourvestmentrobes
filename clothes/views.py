from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from .forms import UserRegisterForm, MessageForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sale, SalesRecord, Testimonial, LikePost, Message
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, View
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account has been created! you are now able to log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def Sales(request):
    sales = Sale.objects.all()

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    sales = Sale.objects.filter(
        Q(title__icontains=q)
    )

    paginator = Paginator(sales, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    sales_record = SalesRecord.objects.all()
    testimony = Testimonial.objects.all()
    paginate = Paginator(testimony, 3)
    page = request.GET.get('page')
    try:
        testimony = paginate.page(page)
    except PageNotAnInteger:
        testimony = paginate.page(1)
    except EmptyPage:
        testimony = paginate.page(paginate.num_pages)



    context = {
        'sales':sales, 'sales_record' : sales_record,  'page':page, 'testimony':testimony,
        'page_obj':page_obj}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def messageSale(request, pk):
    sale = get_object_or_404(Sale, id=pk)
    sale_messages = sale.message_set.all()
    paginator = Paginator(sale_messages, 2)
    page = request.GET.get('page')
    try:
        sale_messages = paginator.page(page)
    except PageNotAnInteger:
        sale_messages = paginator.page(1)
    except EmptyPage:
        sale_messages = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            sale=sale,
            body=request.POST.get('body')
        )
        return redirect('sale', pk=sale.id)
    context = {'sale': sale, 'sale_messages': sale_messages, }
    return render(request, 'sale.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    users = message.sale

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('sale', pk=users.id)
    return render(request, 'delete.html', {'obj': message})

def updateMessage(request, pk):
    message = Message.objects.get(id=pk)
    users = message.sale
    comment = get_object_or_404(Message, id=pk, user=request.user)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('sale', pk=users.id)
    else:
        form = MessageForm(instance=comment)
    return render(request, 'edit_message.html', {'form':form})


def search(request):
    query = request.GET.get("q")
    if query:
        sales = Sale.objects.filter(Q(title__icontains=query) | Q(price__icontains=query))
    else:
        sales = Sale.objects.all()
    # context = {school: school}
    return render(request, 'search.html', {"sales": sales})


def salesDetail(request, pk):
    sales = get_object_or_404(Sale, id=pk)
    sales_record = SalesRecord.objects.all()
    Sales = Sale.objects.all()
    context = {
        'sales': sales,
        'sales_record' : sales_record,
        'Sales': Sales

    }
    return render(request, 'sales_detail.html', context)

class SalesCreateView(CreateView):
    model = Sale
    template_name = 'sales_form.html'
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SalesUpdateView(UpdateView):
    model = Sale
    template_name = 'sales_update.html'
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class SalesDeleteView(DeleteView):
    model = Sale
    template_name = 'sales_delete.html'
    success_url = '/'

    def test_func(self):
        sale = self.get_object()
        if self.request.user == sale.author:
            return True
        return False

def salesRecords(request):
    salesRecord = SalesRecord.objects.all()
    context = {
        'salesRecord':salesRecord
    }
    return render(request, 'home.html', context)


def salesRecordsDetail(request, pk):
    salesRecord = get_object_or_404(SalesRecord, id=pk)
    context = {
        'sales': salesRecord
    }
    return render(request, 'salesRecord_detail.html', context)

class SalesRecordCreateView(CreateView):
    model = SalesRecord
    template_name = 'salesRecord_form.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SalesRecordUpdateView(UpdateView):
    model = SalesRecord
    template_name = 'salesRecord_update.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class SalesRecordDeleteView(DeleteView):
    model = SalesRecord
    template_name = 'salesRecord_delete.html'
    success_url = '/'

    def test_func(self):
        sale = self.get_object()
        if self.request.user == sale.author:
            return True
        return False

############

def testimonialDetail(request, pk):
    testimony_detail = get_object_or_404(Testimonial, id=pk)
    context = {
        'testimony_detail': testimony_detail
    }
    return render(request, 'testimony_detail.html', context)

class TestimonialCreateView(CreateView):
    model = Testimonial
    template_name = 'testimony_form.html'
    fields = ['name', 'title', 'Bio', 'test_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TestimonialUpdateView(UpdateView):
    model = Testimonial
    template_name = 'testimony_update.html'
    fields = ['name', 'title', 'Bio', 'test_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TestimonialDeleteView(DeleteView):
    model = Testimonial
    template_name = 'testimony_delete.html'
    success_url = '/'

    def test_func(self):
        sale = self.get_object()
        if self.request.user == sale.author:
            return True
        return False
@login_required(login_url='login')
def like_sale(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    sales = Sale.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        sales.no_of_likes =sales.no_of_likes+1
        sales.save()
        return redirect('/')
    else:
        like_filter.delete()
        sales.no_of_likes = sales.no_of_likes-1
        sales.save()
        return redirect('/')