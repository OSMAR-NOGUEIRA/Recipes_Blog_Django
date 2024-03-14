import math
from django.core.paginator import Paginator


def make_pagination_range(
        page_range,
        qty_pages,             
        current_page,
):
    total_pages = page_range[-1]

    if (current_page >= math.ceil(qty_pages/2)) and (current_page <= (total_pages - int(qty_pages/2))):
        middle_range = current_page
    elif current_page >= (total_pages - int(qty_pages/2)):
        middle_range = total_pages - int(qty_pages/2)
    else:
        middle_range = math.ceil(qty_pages/2)

    start_range = int(middle_range - (qty_pages/2)) 
    stop_range = int(middle_range + (qty_pages/2))
    
    pagination = page_range[start_range:stop_range]

    first_page_out_of_range = (1 not in pagination)
    last_page_out_of_range = (total_pages not in pagination)

    return {
        'pagination':pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range':start_range,
        'stop_range':stop_range,
        'first_page_out_of_range': first_page_out_of_range ,
        'last_page_out_of_range': last_page_out_of_range,
    }

def make_pagination(request, queryset, itens_per_page, qty_pages=5):

    try :
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(queryset, itens_per_page)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        qty_pages,
        current_page
    )

    return page_obj, pagination_range