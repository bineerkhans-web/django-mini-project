from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Plot, PlotImage

@login_required(login_url='myapp:signin')
def upload(request):
    return render(request, 'pages/upload.html')

@login_required(login_url='myapp:signin')
def myplot(request):
    user_plots = Plot.objects.filter(owner=request.user).prefetch_related('images').order_by('-created_at')

    if not user_plots.exists():
        match_conditions = Q()

        username = (request.user.username or '').strip()
        full_name = (request.user.get_full_name() or '').strip()
        user_phone = getattr(request.user, 'phone', '') or ''
        user_phone = user_phone.strip()

        if username:
            match_conditions |= Q(seller_name__iexact=username)

        if full_name and full_name.lower() != username.lower():
            match_conditions |= Q(seller_name__iexact=full_name)

        if user_phone:
            match_conditions |= Q(seller_phone=user_phone)

        if match_conditions:
            fallback_plots = Plot.objects.filter(owner__isnull=True).filter(match_conditions)
            if fallback_plots.exists():
                fallback_plots.update(owner=request.user)
                user_plots = Plot.objects.filter(owner=request.user).prefetch_related('images').order_by('-created_at')

    context = {
        'plots': user_plots
    }
    return render(request, 'pages/myplot.html', context)

@login_required(login_url='myapp:signin')
def update_plot(request, plot_id):
    try:
        plot = Plot.objects.get(id=plot_id, owner=request.user)
    except Plot.DoesNotExist:
        messages.error(request, 'Plot not found or you do not have permission to edit it.')
        return redirect('secondapp:myplot')

    if request.method == 'POST':
        seller_name = request.POST.get('seller_name', '').strip()
        seller_phone = request.POST.get('seller_phone', '').strip()
        title = request.POST.get('title', '').strip()
        location = request.POST.get('location', '').strip()
        cent = request.POST.get('cent', '')
        price = request.POST.get('price', '')
        description = request.POST.get('description', '').strip()

        if not all([seller_name, seller_phone, title, location, cent, price, description]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('secondapp:myplot')

        try:
            plot.seller_name = seller_name
            plot.seller_phone = seller_phone
            plot.title = title
            plot.location = location
            plot.cent = float(cent)
            plot.price = float(price)
            plot.description = description
            plot.save()
            messages.success(request, 'Plot updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating plot: {e}')

    return redirect('secondapp:myplot')

@login_required(login_url='myapp:signin')
def delete_plot(request, plot_id):
    try:
        plot = Plot.objects.get(id=plot_id, owner=request.user)
    except Plot.DoesNotExist:
        messages.error(request, 'Plot not found or you do not have permission to delete it.')
        return redirect('secondapp:myplot')

    if request.method == 'POST':
        plot.delete()
        messages.success(request, 'Plot deleted successfully.')
        return redirect('secondapp:myplot')

    return redirect('secondapp:myplot')

@login_required(login_url='myapp:signin')
def plotsale(request):
    if request.method == 'POST':
        try:
            
            seller_name = request.POST.get('seller_name', '').strip()
            seller_phone = request.POST.get('seller_phone', '').strip()
            title = request.POST.get('title', '').strip()
            location = request.POST.get('location', '').strip()
            cent = request.POST.get('cent', '')
            price = request.POST.get('price', '')
            description = request.POST.get('description', '').strip()
            map_address = request.POST.get('map_address', '').strip()
            images = request.FILES.getlist('images')
            
           
            if not all([seller_name, seller_phone, title, location, cent, price, description]):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('secondapp:upload')
            
            if not images:
                messages.error(request, 'Please upload at least one image.')
                return redirect('secondapp:upload')
            
            
            plot = Plot.objects.create(
                owner=request.user,
                seller_name=seller_name,
                seller_phone=seller_phone,
                title=title,
                location=location,
                cent=float(cent),
                price=float(price),
                description=description,
                map_address=map_address or None
            )
            
            
            for image in images:
                PlotImage.objects.create(plot=plot, image=image)
            
            messages.success(request, 'Plot uploaded successfully!')
            return redirect('secondapp:upload')
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('secondapp:upload')
    
    return redirect('secondapp:upload')