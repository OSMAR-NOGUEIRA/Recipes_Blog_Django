from unittest import TestCase
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def  test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5, 
            current_page=6,
        )['pagination']
        self.assertEqual([4,5,6,7,8], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        # CURRENT PAGE = 1   -   MIDDLE-PAGE = 3
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=1,
        )['pagination']
        self.assertEqual([1,2,3,4,5], pagination)


        # CURRENT PAGE = 2   -   MIDDLE-PAGE = 3
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=2,
        )['pagination']
        self.assertEqual([1,2,3,4,5], pagination)


        # CURRENT PAGE = 3   -   MIDDLE-PAGE = 3
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=3,
        )['pagination']
        self.assertEqual([1,2,3,4,5], pagination)


        # CURRENT PAGE = 4   -   MIDDLE-PAGE = 4
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=4,
        )['pagination']
        self.assertEqual([2,3,4,5,6], pagination)


        # CURRENT PAGE = 5   -   MIDDLE-PAGE = 5
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=5,
        )['pagination']
        self.assertEqual([3,4,5,6,7], pagination)

        # CURRENT PAGE = 6   -   MIDDLE-PAGE = 6
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=6,
        )['pagination']
        self.assertEqual([4,5,6,7,8], pagination)
        

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        # CURRENT PAGE = 18   -   MIDDLE-PAGE = 18
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=18,
        )['pagination']
        self.assertEqual([16,17,18,19,20], pagination)


        # CURRENT PAGE = 19   -   MIDDLE-PAGE = 18
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=19,
        )['pagination']
        self.assertEqual([16,17,18,19,20], pagination)


        # CURRENT PAGE = 20   -   MIDDLE-PAGE = 18
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=20,
        )['pagination']
        self.assertEqual([16,17,18,19,20], pagination)




