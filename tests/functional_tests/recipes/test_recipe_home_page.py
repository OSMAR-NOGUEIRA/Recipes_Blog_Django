from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from unittest.mock import patch

from .base import RecipeBaseFunctionalTest
from utils.generateFakes import make_batch_of_recipes


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_index__no_recipes_found__message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('You have no recipes to be shown yet.', body.text)
        
    def test_recipe_search_can_find_correct_recipes(self):
        title_needed = 'recipe title maching for search'
        make_batch_of_recipes(qty_recipes=10, first_recipe_title=title_needed)
        
        #user open the page
        self.browser.get(self.live_server_url)
        
        #see a input camp with the text 'Search for recipes here'
        search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Search for recipes here."]')
        
        #clicking in the input
        #search_input.click()
        
        #typing the recipe's title term for a search and pressing enter
        search_input.send_keys('recipe title maching for search')
        search_input.send_keys(Keys.ENTER)
        
        body = self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        
        self.assertIn('recipe title maching for search', body)
        
    @patch('recipes.views.recipe_views.PER_PAGE', new=2)
    def test_recipe_home_index_pagination(self):
        make_batch_of_recipes()
        
        #user open the page
        self.browser.get(self.live_server_url)
        
        #see that there are pagination options and click on option page 2
        page2 = self.browser.find_element(By.XPATH, '//a[@aria-label="Go to page 2"]')
        page2.click()
        
        #see that there are 2 recipes in the page 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 
            2
        )
        

