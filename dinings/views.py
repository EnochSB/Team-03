from django.shortcuts import render, redirect
from .models import Dining, Review, Menu, PurposeTag, AtmosphereTag, FacilityTag
from .forms import DiningForm, ReviewForm, MenuForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import JsonResponse
from collections import defaultdict
import random
import requests, json, pprint
from team_03 import settings

# Create your views here.
def get_address(lat, lng):
    url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x="+lng+"&y="+lat
    # 'KaKaoAK '는 그대로 두시고 개인키만 지우고 입력해 주세요.
    # ex) KakaoAK 6af8d4826f0e56c54bc794fa8a294
    headers = {"Authorization": f"KakaoAK {settings.KAKAO_KEY}"}
    api_json = requests.get(url, headers=headers)
    full_address = json.loads(api_json.text)


    return full_address


def index(request):
    
    # url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={settings.GOOGLE_KEY}'
    # data = {
    #     'considerIp': True,
    # }

    # result = requests.post(url, data).text
    # result = eval(result)
    # full_address = get_address(str(result['location']['lat']), str(result['location']['lng']))
    # my_location = full_address['documents'][0]['region_3depth_name']
    # print(my_location)

    region = request.GET.get('region')
    region_search_param = request.GET.get('region_search')
    is_selected = False
    select_region = region_search_param = request.GET.get('region_search')

    if region:
        region_dinings = Dining.objects.filter(Q(address_gu__icontains=region) | Q(
        address_dong__icontains=region)).distinct()
    elif region_search_param:
        region_dinings = Dining.objects.filter(Q(address_gu__icontains=region_search_param) | Q(
        address_dong__icontains=region_search_param)).distinct()
        is_selected = True
    else:
        region_dinings = Dining.objects.none()
    dinings = Dining.objects.order_by("-pk")

     # query for dinings
    count = dinings.count()

    if count < 20:
        # if there are less than 20 dinings, show all of them
        dinings = dinings.all()
    else:
        # if there are more than 20 dinings, randomly sample 20 of them
        dinings = random.sample(list(dinings), 20)

    # get tags
    tags = list(set(tag for dining in dinings for tag in dining.tags.all()))
    random_tags = random.sample(tags, min(len(tags), 10))

    tags = list(set(tag for dining in dinings for tag in dining.tags.all()))
    random_tags = random.sample(tags, min(len(tags), 10))
    context = {
        'dinings': dinings,
        'tags': random_tags,
        # 'my_location': my_location,
        'region_dinings': region_dinings,
        'is_selected': is_selected,
        'select_region': select_region,
    }
    return render(request, 'dinings/index.html', context)


# def index(request):
#     dinings = Dining.objects.order_by("-pk")
#     tags = []
#     for dining in dinings:
#         tags += dining.tags.all().distinct()
#     context = {
#         'dinings': dinings,
#         'tags': tags,
#     }
#     return render(request, 'dinings/index.html', context)


def showmap(request):
    locality = request.GET.get('locality', '')
    context = {'locality': locality}
    return render(request, 'dinings/showmap.html', context)


def detail(request, pk):
    dining = Dining.objects.get(pk=pk)
    reviews = dining.review_set.all()
    menu_form = MenuForm(request.POST)
    menus = dining.menu_set.all()

    sum = 0
    avg = 0

    #만족도 담을 딕셔너리
    satisfaction = {
        '매우만족': 0,
        '만족': 0,
        '보통': 0,
        '불만': 0,
        '매우불만': 0,
    }

    # zero division error 때문에 조건문 추가
    if reviews:
        for review in reviews:
            sum += review.rating
            if review.rating > 4:
                satisfaction['매우만족'] += 1
            elif review.rating > 3:
                satisfaction['만족'] += 1
            elif review.rating > 2:
                satisfaction['보통'] += 1
            elif review.rating > 1:
                satisfaction['불만'] += 1
            else:
                satisfaction['매우불만'] += 1
        # 총 평점을 나타내기 위해 avg 변수에 평균 할당
        avg = round(sum / len(reviews), 1)
    context = {
        'dining': dining,
        'reviews': reviews,
        'avg': avg,
        'menus': menus,
        'menu_form': menu_form,
        'satisfaction': satisfaction,
    }
    return render(request, 'dinings/detail.html', context)

def dining_create(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = DiningForm(request.POST, request.FILES) 
            if form.is_valid():
                dining = form.save(commit=False)
                dining.address_postcode = request.POST['address_postcode']
                dining.address_address = request.POST['address_address']

                
                gu = [ele for ele in request.POST['address_address'].split() if ele[-1] == '구']
                if gu:
                    dining.address_gu = gu[0]
                
                dong = [ele for ele in request.POST['address_address'].split() if ele[-1] == '동' or ele[-1] == '읍' or ele[-1] ==
                 '면' or ele[-1] == '리']
                if dong:
                    dining.address_dong = dong[0]

                dining.address_extra = request.POST['address_extra']

                dining.address_detail = request.POST['address_detail']
                dining.address_extra = request.POST['address_extra']
                dining.save()
                form.save_m2m()
                return redirect('dinings:index')
        else:
            form = DiningForm()
        context = {
            'form': form,
        }
    else:
        return redirect('dinings:index')
    return render(request, 'dinings/dining_create.html', context)

# def dining_create(request):
#     if request.user.is_superuser:
#         if request.method == 'POST':
#             form = DiningForm(request.POST, request.FILES)
#             address_postcode = request.POST['address_postcode']
#             address_address = request.POST['address_address']
#             address_extra = request.POST['address_extra']
#             address_detail = request.POST['address_detail']
#             adress = Dining(address_postcode=address_postcode,address_address=address_address,address_extra=address_extra, address_detail=address_detail)
#             if form.is_valid():
#                 form.save()
#                 adress.save()
#                 return redirect('dinings:index')
#         else:
#             form = DiningForm()
#         context = {
#             'form': form,
#         }
#     else:
#         return redirect('dinings:index')
#     return render(request, 'dinings/dining_create.html', context)


@login_required
def review_create(request, dining_pk):
    dining = Dining.objects.get(pk=dining_pk)

    # 리뷰 작성
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            print(review_form.cleaned_data)
            review = review_form.save(commit=False)
            review.user = request.user
            review.dining = dining
            review.rating = request.POST.get('rating')
            review.rating_taste = request.POST.get('rating_taste')
            review.rating_price = request.POST.get('rating_price')
            review.rating_kind = request.POST.get('rating_kind')
            review.save()
            purpose_tag_ids = request.POST.get('purpose_tags').split(',')
            atmosphere_tag_ids = request.POST.get('atmosphere_tags').split(',')
            facility_tag_ids = request.POST.get('facility_tags').split(',')
            review.purpose_tags.set(purpose_tag_ids)
            review.atmosphere_tags.set(atmosphere_tag_ids)
            review.facility_tags.set(facility_tag_ids)
            # for tag_id in purpose_tag_ids:
            #     if tag_id:
            #         review.purpose_tags.create(purposetag_id=tag_id)
            # for tag_id in atmosphere_tag_ids:
            #     if tag_id:
            #         review.atmosphere_tags.create(atmospheretag_id=tag_id)
            # for tag_id in facility_tag_ids:
            #     if tag_id:
            #         review.facility_tags.create(facilitytag_id=tag_id)
            return redirect('dinings:detail', dining.pk)
    # 리뷰 작성 페이지
    else:
        review_form = ReviewForm()
        purpose_tags = PurposeTag.objects.filter(pk__range=(1,19))
        atmosphere_tags = AtmosphereTag.objects.filter(pk__range=(1, 14))
        facility_tags = FacilityTag.objects.filter(pk__range=(1, 10))
    context = {
        'review_form': review_form,
        'dining': dining,
        'purpose_tags': purpose_tags,
        'atmosphere_tags': atmosphere_tags,
        'facility_tags': facility_tags,
    }
    return render(request, 'dinings/review_create.html', context)


@login_required
def review_detail(request, dining_pk, review_pk):
    review = Review.objects.get(pk=review_pk)

    # 리뷰 공감
    if request.method == 'POST':
        dining = Dining.objects.get(pk=dining_pk)
        if dining.like_users.filter(pk=request.user.pk).exists():
            dining.like_users.remove(request.user)
        else:
            dining.like_users.add(request.user)
        return redirect('dinings:detail', dining.pk)

    # 리뷰 삭제
    elif request.method == 'DELETE':
        if request.user == review.user:
            review.delete()
        return redirect('dinings:index')


@login_required
def review_update(request, dining_pk, review_pk):
    review = Review.objects.get(pk=review_pk)

    if request.user == review.user:
        if request.method == 'POST':
            review_form = ReviewForm(
                request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                review_form.save()
                return redirect('dinings:detail', dining_pk)

        else:
            review_form = ReviewForm(instance=review)
    else:
        return redirect('dinings:detail', dining_pk)
    context = {
        'review_form': review_form,
        'dining_pk': dining_pk,
        'review_pk': review_pk,
    }
    return render(request, 'dinings/review_update.html', context)


@login_required
def dining_update(request, dining_pk):
    dining = Dining.objects.get(pk=dining_pk)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = DiningForm(request.POST, instance=dining)
            if form.is_valid():
                form.save()
                return redirect('dinings:detail', dining_pk)
        else:
            form = DiningForm(instance=dining)
    else:
        return redirect('dinings:detail', dining_pk)
    context = {
        'form': form,
        'dining': dining
    }
    return render(request, 'dinings/dining_update.html', context)


@login_required
def dining_delete(request, dining_pk):
    dining = Dining.objects.get(pk=dining_pk)
    if request.user.is_superuser:
        dining.delete()
    else:
        return redirect('dinings:detail', dining_pk)
    return redirect('dinings:index')


def search(request):
    query = request.GET.get('query')
    dinings = Dining.objects.filter(Q(title__icontains=query) | Q(
        tags__name__icontains=query)).distinct()
    dining_reviews = []
    for dining in dinings:
        review = dining.review_set.order_by('pk').first()
        if review:
            dining_reviews.append(review)
    context = {'dinings': dinings,
               'reviews': dining_reviews
               }
    return render(request, 'dinings/search.html', context)


@login_required
def menu_create(request, dining_pk):
    dining = Dining.objects.get(pk=dining_pk)
    menu_form = MenuForm(request.POST)

    if request.user.is_superuser:
        if menu_form.is_valid():
            menu = menu_form.save(commit=False)
            menu.dining = dining
            menu.save()
            name = menu.name
            price = menu.price
            context = {
                'name': name,
                'price': price
            }
            return JsonResponse(context)
    else:
        return redirect('dinings:detail', dining_pk)

    context = {
        'dining': dining,
        'menu_form': menu_form,
    }
    return render(request, 'dinings/detail.html', context)


@login_required
def likes(request, dining_pk):
    dining = Dining.objects.get(pk=dining_pk)

    if dining.like_users.filter(pk=request.user.pk).exists():
        dining.like_users.remove(request.user)
        is_liked = False
    else:
        dining.like_users.add(request.user)
        is_liked = True

    context = {
        'is_liked': is_liked,
        'like_count': dining.like_users.count(),
    }
    return JsonResponse(context)


@login_required
def review_delete(request, dining_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()
    return redirect('dinings:detail', dining_pk)


@login_required
def review_like(request, dining_pk, review_pk):
    review = Review.objects.get(pk=review_pk)

    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
    else:
        review.like_users.add(request.user)
    return redirect('dinings:detail', dining_pk)


@login_required
def menu_delete(request, dining_pk, menu_pk):
    menu = Menu.objects.get(pk=menu_pk)
    if request.user.is_superuser:
        menu.delete()
    return redirect('dinings:detail', dining_pk)
