from unittest import TestCase               # USANDO O TestCase DO unittest PARA ALGUNS TESTES, PQ O TestCase DO DAJNGO E' MAIS COMPLETO MAS E' MAIS DEVAGAR TAMBEM E COMO ESTAMOS TESTANDO O FORM DIRETAMENTE NAO PRECISAMOS DE COISAS PROPRIAS DO DJANGO

from django.test import TestCase as DjangoTestCase
from django.urls import reverse

from authors.forms import RegisterForm
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'e.g. user01+'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password here'),
        ('first_name', 'e.g. John'),
        ('last_name', 'e.g. Conor'),
        ('email', 'e.g. email@email.com'),
    ])
    def test_fields_placeholder(self, field, value_test):
        form = RegisterForm()
        current_field_value = form[field].field.widget.attrs['placeholder']
        self.assertEqual(value_test, current_field_value)


    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Check password'),
    ])
    def test_fields_label(self, field, value_test):
        form = RegisterForm()
        current_field_value = form[field].field.label
        self.assertEqual(value_test, current_field_value)


    @parameterized.expand([
        ('password', ('Password must have at least one uppercase letter, '
                     'one lowercase letter and one number. The length should be '
                     'at least 8 characters.')),
        ('password2', ('Password must have at least one uppercase letter, '
                      'one lowercase letter and one number.')),
        ('email', 'The Email must be valid.'),
    ])
    def test_fields_help_text(self, field, value_test):
        form = RegisterForm()
        current_field_value = form[field].field.help_text
        self.assertEqual(value_test, current_field_value)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username':'user',
            'first_name':'first',
            'last_name':'last',
            'email':'email@email.com',
            'password':'Str0ngP@ssword',
            'password2':'Str0ngP@ssword',
        }
        return super().setUp(*args, **kwargs)
    
    def test_authors_view_create_raises_404_if_request_not_post(self):
        response = self.client.get(reverse('authors:register_create'))
        status_code = response.status_code

        self.assertEqual(status_code, 404)
    

    def test_fields_username_cannot_be_empty(self):
        msg = 'This field can not be empty.'
        self.form_data['username'] = ''
        url = reverse('authors:register_create')

        response = self.client.post(url, data=self.form_data, follow=True)  #follow foi usado pq a view authors:register_create fas um redirecionamento para a view authors:register
        
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_fields_first_name_cannot_be_empty(self):
        msg = 'First name is required.'
        self.form_data['first_name'] = ''

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        error = response.context['form'].errors.get('first_name')
        
        self.assertIn(msg, error)

    def test_fields_last_name_cannot_be_empty(self):
        msg = 'Last name is required.'
        url = reverse('authors:register_create')
        self.form_data['last_name'] = ''

        response = self.client.post(url, data=self.form_data, follow=True)
        error = response.context['form'].errors.get('last_name')
        self.assertIn(msg, error)

    def test_fields_email_cannot_be_empty(self):
        msg = 'E-mail is required.'
        url = reverse('authors:register_create')
        self.form_data['email'] = ''

        response = self.client.post(url, data=self.form_data, follow=True)
        error = response.context['form'].errors.get('email')
        self.assertIn(msg, error)

    def test_fields_password_cannot_be_empty(self):
        msg = 'Password must not be empty.'
        url = reverse('authors:register_create')
        self.form_data['password'] = ''

        response = self.client.post(url, data=self.form_data, follow=True)
        error = response.context['form'].errors.get('password')
        self.assertIn(msg, error)

    def test_fields_password2_cannot_be_empty(self):
        msg = 'Please repeat your password.'
        url = reverse('authors:register_create')
        self.form_data['password2'] = ''

        response = self.client.post(url, data=self.form_data, follow=True)
        error = response.context['form'].errors.get('password2')

        self.assertIn(msg, error)

    def test_fields_username_min_length_should_be_4(self):
        msg = 'Ensure this value has at least 4 characters (it has 3).'
        url = reverse('authors:register_create')
        self.form_data['username'] = 'use'

        response = self.client.post(url, data=self.form_data, follow=True)
        error = response.context['form'].errors.get('username')

        self.assertIn(msg, error)

    def test_fields_username_max_length_must_have_150_chars(self):
        msg = 'Ensure this value has at most 150 characters (it has 151).'
        url = reverse('authors:register_create')
        self.form_data['username'] = 'A' * 151

        response = self.client.post(url, data=self.form_data, follow=True)
        error = response.context['form'].errors.get('username')

        self.assertIn(msg, error)

    def test_password_field_have_lower_upper_case_letters_and_number(self):
        msg = ('Password must have at least one uppercase letter, one lowercase letter and one number. the length must be at least 8 characters.')
        url = reverse('authors:register_create')
        ## Password Invalid 
        self.form_data['password'] = 'a' * 8

        response = self.client.post(url, data=self.form_data, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn(msg, content)
        
        ## Password Valid now
        self.form_data['password'] = 'Str0ngP@ssword'

        response = self.client.post(url, data=self.form_data, follow=True)
        content = response.content.decode('utf-8')

        self.assertNotIn(msg, content)

    def test_fields_password_and_password2_have_same_content(self):
        msg = ('Those passwords didn’t match. Try again.')
        url = reverse('authors:register_create')
        ## Password Invalid 
        self.form_data['password'] = 'Str0ngP@ssword!='
        self.form_data['password2'] = 'Str0ngP@ssword'

        response = self.client.post(url, data=self.form_data, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn(msg, content)
        
        ## Password Valid now
        self.form_data['password'] = 'Str0ngP@ssword'
        self.form_data['password2'] = 'Str0ngP@ssword'

        response = self.client.post(url, data=self.form_data, follow=True)
        content = response.content.decode('utf-8')

        self.assertNotIn(msg, content)

    def test_fields_password_message_error__type_a_strong_password__ok(self):
        msg = ('Type a stronger password.')
        url = reverse('authors:register_create')
        ## Password Invalid 
        self.form_data['password'] = '12345678'
        self.form_data['password2'] = '12345678'

        response = self.client.post(url, data=self.form_data, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn(msg, content)
        
        ## Password Valid now
        self.form_data['password'] = 'Str0ngP@ssword'
        self.form_data['password2'] = 'Str0ngP@ssword'

        response = self.client.post(url, data=self.form_data, follow=True)
        content = response.content.decode('utf-8')

        self.assertNotIn(msg, content)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')
        msg = 'Email is already in use.'

        self.client.post(url, data=self.form_data, follow=True)

        #creating another user using same email
        response = self.client.post(url, data=self.form_data, follow=True)
        content = response.content.decode('utf-8')
        context = response.context['form'].errors.get('email')

        self.assertIn(msg, content)
        self.assertIn(msg, context)

    def test_author_create_can_login(self):
        url = reverse('authors:register_create')

        self.form_data.update({
            'username': 'userTest',
            'password':'StrongPass123',
            'password2':'StrongPass123',
        })

        self.client.post(url, data=self.form_data, follow=True)
        is_authenticated = self.client.login(
            username='userTest',
            password='StrongPass123'
            )
        self.assertTrue(is_authenticated)
