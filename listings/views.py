from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from listings.choices import price_choices, bedrooom_choices, region_choices

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)



    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    house_count= Listing.objects.filter(is_published=True).count()

    context = {
        'listings': paged_listings,
        'nyumba_jumla': house_count
    }
    return render(request, 'listings/listings.html' , context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html' ,context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    #Keywords ; hiki kipande cha filter
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    #city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
            #iexact ni case insensitive

    #region
    if 'region' in request.GET:
        region = request.GET['region']
        if region:
            queryset_list = queryset_list.filter(region__iexact=region)

    #bedrooms
    if 'bedroooms' in request.GET:
        bedroooms = request.GET['bedroooms']
        if bedroooms:
            queryset_list = queryset_list.filter(bedroooms__lte=bedroooms)

    #price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'listings': queryset_list ,
        'region_choices': region_choices ,
        'bedroom_choices': bedrooom_choices ,
        'price_choices': price_choices ,
        'values': request.GET
    }

    return render(request, 'listings/search.html' ,context)




