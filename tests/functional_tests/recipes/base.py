from django.test import LiveServerTestCase              #Para uso em testes q necessitem do servidor (este teste sobe o servidor sem os arquivos estaticos como css)
import time

from utils.browser import make_chrome_browser
from recipes.tests.test_recipe_base import RecipeMixin

class RecipeBaseFunctionalTest(LiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_chrome_browser('--headless') # '--headless'
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)
