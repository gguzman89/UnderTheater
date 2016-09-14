# vim: set fileencoding=utf-8 :
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.phantomjs.webdriver import WebDriver as PhatomWebDriver
from underTheaterApp.factories import PlayTheaterFactory, UserFactory
from underTheaterApp.models import PlayTheater
from django.contrib.auth.hashers import make_password


class BaseSeleniumTests(StaticLiveServerTestCase):
    webs_driver = {"phatom": PhatomWebDriver,
                   "chrome": ChromeWebDriver,
                   "firefox": FirefoxWebDriver}
    driver_type = "phatom"

    @classmethod
    def setUpClass(cls):
        super(BaseSeleniumTests, cls).setUpClass()
        cls.selenium = cls.webs_driver[cls.driver_type]()
        cls.selenium.set_window_size(1024, 768)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(BaseSeleniumTests, cls).tearDownClass()

    def open(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))


class SearchViewTestsCase(BaseSeleniumTests):
    driver_type = "phatom"

    def test_search_a_play_theater(self):
        "Test que prueba la busqueda de obras de teatro"
        # Creo una obra de teatro
        play_theater = PlayTheaterFactory.create(play_name="El pais")

        # Entro a la app
        self.open()

        # Lleno el buscador con el nombre de la obra a buscar
        search_form = self.selenium.find_element_by_css_selector("#search_form")
        search_input = search_form.find_element_by_css_selector(".search_term")
        search_input.clear()
        search_input.send_keys(play_theater.play_name)
        search_form.find_element_by_css_selector('button[type="submit"]').click()

        # Se redirige a otra pagina con los resultados de la busquesda
        search_result = self.selenium.find_element_by_name(play_theater.pk)

        # Entonces deberia mostrar la obra a buscar
        self.assertTrue(search_result.is_displayed())
        self.assertEqual(search_result.text, play_theater.play_name)

    def test_search_but_not_find_any_play_theater(self):
        """
        Test que prueba la busqueda de obras de teatro cuando no hay ninguna
        obra para devolver
        """

        # Creo una obra de teatro
        PlayTheaterFactory.create(play_name="El pais")

        # Entro a la app
        self.open()

        # Lleno el buscador con el nombre de la obra a buscar
        search_form = self.selenium.find_element_by_css_selector("#search_form")
        search_input = search_form.find_element_by_css_selector(".search_term")
        search_input.clear()
        search_input.send_keys("No esta en la base")
        search_form.find_element_by_css_selector('button[type="submit"]').click()

        # Se redirige a otra pagina con los resultados de la busquesda
        search_result = self.selenium.find_element_by_css_selector(".alert-danger")

        # Entonces deberia el msj que no encontre ninguna obra
        self.assertTrue(search_result.is_displayed())
        self.assertEqual(search_result.text,
                         "No se encontraron resultados para tu busqueda.")

    def test_search_play_theater_and_returns_two_results(self):
        """
        Test que prueba la busqueda de obras de teatro cuando no hay ninguna
        obra para devolver
        """

        # Creo una obra de teatro
        play_theater_1 = PlayTheaterFactory.create(play_name="Padre millonario")
        play_theater_2 = PlayTheaterFactory.create(play_name="Padre de familia")
        play_theater_3 = PlayTheaterFactory.create(play_name="El pais")

        # Entro a la app
        self.open()

        # Lleno el buscador con el nombre de la obra a buscar
        search_form = self.selenium.find_element_by_css_selector("#search_form")
        search_input = search_form.find_element_by_css_selector(".search_term")
        search_input.clear()
        search_input.send_keys("Padre")
        search_form.find_element_by_css_selector('button[type="submit"]').click()

        # Se redirige a otra pagina con los resultados de la busquesda
        search_result_1 = self.selenium.find_element_by_name(play_theater_1.pk)
        search_result_2 = self.selenium.find_element_by_name(play_theater_2.pk)
        search_result_3 = self.selenium.find_elements_by_name(play_theater_3.pk)

        # Entonces deberia las 2 obras en pantalla
        self.assertTrue(search_result_1.is_displayed())
        self.assertEqual(search_result_1.text, play_theater_1.play_name)

        self.assertTrue(search_result_2.is_displayed())
        self.assertEqual(search_result_2.text, play_theater_2.play_name)

        # y la tercer obra no aparece en los resultados
        self.assertEqual(len(search_result_3), 0)

    def tearDown(self):
        "Borro las imagenes despues de los test"
        for p in PlayTheater.objects.all():
            p.picture.delete()


class LoginAndRegisterViewTestCase(BaseSeleniumTests):

    def _complete_register_form(self, username, email, password, confirm_password=None):

        confirm_password = confirm_password or password

        # Completa el formulario de registro
        register_form = self.selenium.find_element_by_css_selector("#register_form")

        # con un username
        username_input = register_form.find_element_by_css_selector("#id_username")
        username_input.clear()
        username_input.send_keys(username)

        # un email
        email_input = register_form.find_element_by_css_selector("#id_email")
        email_input.clear()
        email_input.send_keys(email)

        # un password
        password = "mipassword12345seis"
        password1_input = register_form.find_element_by_css_selector("#id_password1")
        password1_input.clear()
        password1_input.send_keys(password)

        # y se le pide que confirme el password
        password2_input = register_form.find_element_by_css_selector("#id_password2")
        password2_input.clear()
        password2_input.send_keys(confirm_password)

        # Y por ultimo s e aceptan los cambios
        register_form.find_element_by_css_selector('button[type="submit"]').click()

    def test_a_user_register_in_app(self):
        "Test que registra un usuario en la app"

        # Entra a la app
        self.open()

        # hace click en el boton de loguearse/registrarse
        self.selenium.find_element_by_css_selector("#register").click()
        username = "anUser"

        # completo el formulario de registro
        self._complete_register_form(username, "anUser@dominio.com",
                                     "mipassword12345seis")

        # Entonces se redirige a la pagina principal
        login_menu = self.selenium.find_element_by_css_selector("#login_menu")
        logout_button = self.selenium.find_element_by_css_selector("#logout")

        # con el nombre de usuario en la esquina de la pantalla
        self.assertTrue(login_menu.is_displayed())
        self.assertEqual(login_menu.text, username.upper())

        # y boton para desloguearser activo
        self.assertTrue(logout_button.is_displayed())

    def test_fail_a_user_register_in_app(self):
        "Test que intenta registrar un usuario y falla"

        # Se tiene un usuario registrado en la app
        user = UserFactory.create()

        # Entra a la app
        self.open()

        # hace click en el boton de loguearse/registrarse
        self.selenium.find_element_by_css_selector("#register").click()

        # completo el formulario de registro con un username que ya fue usado
        self._complete_register_form(user.username, user.email,
                                    "mipassword12345seis", "cualquiererda")
        errors = self.selenium.find_elements_by_css_selector(".alert-danger")
        list_errors = [
            u"A user with that username already exists.",
            u"This email already used.",
            u"The two password fields didn't match."
        ]

        for a in errors:
            self.assertTrue(a.is_displayed())
            self.assertTrue(a.text in list_errors)

    def test_a_user_login_in_app(self):
        "Test que loguea un usuario en la app"

        # Se tiene un usuario registrado en la app
        user_password = "unPasswordV1lid0"
        user = UserFactory.create(password=make_password(user_password))

        # Entra a la app
        self.open()

        # hace click en el boton de loguearse/registrarse
        self.selenium.find_element_by_css_selector("#login").click()

        # Se llena el formulario de login
        login_form = self.selenium.find_element_by_css_selector("#login_form")

        # complata con un username
        username_input = login_form.find_element_by_css_selector("#id_username")
        username_input.clear()
        username_input.send_keys(user.username)

        # un password
        password1_input = login_form.find_element_by_css_selector("#id_password")
        password1_input.clear()
        password1_input.send_keys(user_password)

        # Y por ultimo s e aceptan los cambios
        login_form.find_element_by_css_selector('button[type="submit"]').click()

        # Entonces se redirige a la pagina principal
        login_menu = self.selenium.find_element_by_css_selector("#login_menu")
        logout_button = self.selenium.find_element_by_css_selector("#logout")

        # con el nombre de usuario en la esquina de la pantalla
        self.assertTrue(login_menu.is_displayed())
        self.assertEqual(login_menu.text, user.username.upper())

        # y boton para desloguearser activo
        self.assertTrue(logout_button.is_displayed())

    def test_fail_a_user_login_in_app(self):
        "Test que comprueba el mal logueo en al app"

        # Se tiene un usuario registrado en la app
        user_password = "unPasswordV1lid0"
        user = UserFactory.create(password=make_password(user_password))

        # Entra a la app
        self.open()

        # hace click en el boton de loguearse/registrarse
        self.selenium.find_element_by_css_selector("#login").click()

        # Se llena el formulario de login
        login_form = self.selenium.find_element_by_css_selector("#login_form")

        # complata con un username
        username_input = login_form.find_element_by_css_selector("#id_username")
        username_input.clear()
        username_input.send_keys(user.username)

        # un password
        password1_input = login_form.find_element_by_css_selector("#id_password")
        password1_input.clear()
        password1_input.send_keys("cualquier pass")

        # Y por ultimo s e aceptan los cambios
        login_form.find_element_by_css_selector('button[type="submit"]').click()
        alert_error = self.selenium.find_element_by_css_selector(".alert-danger")

        self.assertTrue(alert_error.is_displayed())
        self.assertEqual(alert_error.text,
                         u"Please enter a correct username and password. Note that both fields may be case-sensitive.")
