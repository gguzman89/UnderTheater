# vim: set fileencoding=utf-8 :
import time
import os
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.phantomjs.webdriver import WebDriver as PhatomWebDriver
from underTheaterApp.factories import PlayTheaterFactory, UserFactory, OwnerTheaterFactory,\
    TheaterFactory, RoomTheaterFactory, ActorFactory
from underTheaterApp.users import OwnerTheater, Actor, Spectators
from underTheaterApp.models import PlayTheater
from django.contrib.auth.hashers import make_password
from django.core.cache import cache


class BaseSeleniumTests(StaticLiveServerTestCase):
    webs_driver = {"phatom": PhatomWebDriver,
                   "chrome": ChromeWebDriver,
                   "firefox": FirefoxWebDriver}
    driver_type = "phatom"

    def setUp(self):
        super(BaseSeleniumTests, self).setUp()
        self.selenium = self.webs_driver[self.driver_type]()
        self.addCleanup(self.selenium.quit)
        self.selenium.maximize_window()
        self.selenium.implicitly_wait(10)

    def open(self, url=None):
        url = url if url else '/'
        self.selenium.get('%s%s' % (self.live_server_url, url))

    def click_select_option(self, id, option):
        element = self.selenium.find_element_by_css_selector(id)
        all_options = element.find_elements_by_tag_name("option")
        for opt in all_options:
            if opt.text == option:
                opt.click()

    def upload_image(self, id):
        TEST_IMAGE = os.path.join(settings.STATICFILES_DIRS[0], "logo.png")
        picture_input = self.selenium.find_element_by_css_selector(id)
        picture_input.clear()
        picture_input.send_keys(TEST_IMAGE)

    def login_user(self, user_login=None, password=None):

        # Se tiene un usuario registrado en la app
        user_password = password if password else "unPasswordV1lid0"
        user = user_login if user_login else UserFactory.create(password=make_password(user_password))
        # Entra a la app
        self.open("/accounts/login/")

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

        return user


class SearchViewTestsCase(BaseSeleniumTests):
    driver_type = "firefox"

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
        self.assertEqual(search_result.text, play_theater.play_name.upper())

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
        self.assertEqual(search_result_1.text, play_theater_1.play_name.upper())

        self.assertTrue(search_result_2.is_displayed())
        self.assertEqual(search_result_2.text, play_theater_2.play_name.upper())

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
        password1_input.send_keys(password)

        # y se le pide que confirme el password
        password2_input = register_form.find_element_by_css_selector("#id_password2")
        password2_input.clear()
        password2_input.send_keys(confirm_password)

        # Y por ultimo s e aceptan los cambios
        register_form.find_element_by_css_selector('button[type="submit"]').click()
        user = User.objects.get(username=username)
        OwnerTheaterFactory(user=user)
        self.open()

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

        time.sleep(1)

        OwnerTheaterFactory(user=user)
        self.open()

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

    def tearDown(self):
        cache.clear()


class CreatePublicationViewTestsCase(BaseSeleniumTests):
    driver_type = "firefox"

    def setUp(self):
        super(CreatePublicationViewTestsCase, self).setUp()
        self.theater = TheaterFactory.create()
        self.room_theater = RoomTheaterFactory(theater=self.theater)
        self.actor = ActorFactory.create()

    def _complete_new_publication(self, create_play_form):

        # completa con nombre de obra
        title = "Juan baila"
        play_name_input = create_play_form.find_element_by_css_selector("#id_play_name")
        play_name_input.clear()
        play_name_input.send_keys(title)

        # una sypnosis
        sinopsis = "una obra muy entretenida"
        synopsis_input = create_play_form.find_element_by_css_selector("#id_synopsis")
        synopsis_input.clear()
        synopsis_input.send_keys(sinopsis)

        # un teatro
        self.click_select_option("#id_dayfunction_related-0-theater", self.theater.name)

        # un actor
        self.click_select_option("#id_actors", self.actor.get_complete_name)

        # un precio
        ticket_name = "Jubilados"
        price_name_input = create_play_form.find_element_by_css_selector("#id_ticket_prefix-0-ticket_name")
        price_name_input.clear()
        price_name_input.send_keys(ticket_name)

        price = "200"
        price_input = create_play_form.find_element_by_css_selector("#id_ticket_prefix-0-price")
        price_input.clear()
        price_input.send_keys(price)

        self.upload_image("#id_picture")

        return price, ticket_name, title, sinopsis

    def _check_play_detail_view(self, play, title, ticket_name, price, since_date, hour):
        detail_title = self.selenium.find_element_by_tag_name("h1")
        ticket = play.tickets()[0]
        play_url = "/play_theater/%s/" % play.id
        actor = play.all_actors()[0]
        day_function = play.day_functions()[0]

        self.assertEqual(title.upper(), detail_title.text)
        self.assertTrue(play_url in self.selenium.current_url)
        self.assertEqual(play.play_name, title)
        self.assertEqual(ticket.ticket_name, ticket_name)
        self.assertEqual(ticket.price, price)
        self.assertEqual(actor.get_complete_name, self.actor.get_complete_name)
        self.assertEqual(day_function.theater.name, self.theater.name)
        self.assertEqual(day_function.room_theater.room_name, self.room_theater.room_name)
        self.assertEqual(day_function.datetime_function.since.strftime("%d/%m/%Y"), since_date)
        self.assertTrue(hour in day_function.datetime_function.hours())

    def test_create_a_new_play_publication_with_only_date(self):

        self.login_user()

        # hace click en el boton para crear obra
        self.selenium.find_element_by_css_selector("#create_play").click()
        create_play_form = self.selenium.find_element_by_css_selector("#create_play_form")
        price, ticket_name, title, sinopsis = self._complete_new_publication(create_play_form)

        # un tipo de fecha
        self.click_select_option("#select_datefunction", u"Fecha única")

        # una hora
        hour = "12:30"
        self.click_select_option("#id_hour", hour)

        # una fecha
        date = "11/03/2016"
        date_input = create_play_form.find_element_by_css_selector("#id_since")
        date_input.clear()
        date_input.send_keys(date)

        # Y por ultimo se aceptan los cambios
        create_play_form.find_element_by_css_selector('button[type="submit"]').click()

        time.sleep(1)

        # Entonces se redirige a la pagina de detalles de obra y el objecto obra
        # se tiene que haber creado
        play = PlayTheater.objects.get(play_name=title)

        self._check_play_detail_view(play, title, ticket_name, price, date, hour)

    def test_create_a_new_play_publication_with_periodic_date(self):

        self.login_user()

        # hace click en el boton para crear obra
        self.selenium.find_element_by_css_selector("#create_play").click()
        create_play_form = self.selenium.find_element_by_css_selector("#create_play_form")

        price, ticket_name, title, sinopsis = self._complete_new_publication(create_play_form)

        # un tipo de fecha
        self.click_select_option("#select_datefunction", u"Fecha periódica")

        # una hora
        hour = "12:30"
        self.click_select_option("#id_hour", hour)

        # una fecha
        since_date = "11/03/2016"
        date_input = create_play_form.find_element_by_css_selector("#id_since")
        date_input.clear()
        date_input.send_keys(since_date)

        # una fecha
        until_date = "23/03/2016"
        until_date_input = create_play_form.find_element_by_css_selector("#id_until")
        until_date_input.clear()
        until_date_input.send_keys(until_date)

        # dia de la semana
        periodic = "Lunes"
        self.click_select_option("#id_periodic_date", periodic)

        # Y por ultimo se aceptan los cambios
        create_play_form.find_element_by_css_selector('button[type="submit"]').click()

        time.sleep(1)

        # Entonces se redirige a la pagina de detalles de obra y el objecto obra
        # se tiene que haber creado
        play = PlayTheater.objects.get(play_name=title)
        day_function = play.day_functions()[0]
        self._check_play_detail_view(play, title, ticket_name, price, since_date, hour)

        self.assertEqual(day_function.datetime_function.until.strftime("%d/%m/%Y"), until_date)
        self.assertTrue(periodic in day_function.datetime_function.periodic_dates())

    def test_fail_create_a_new_play_publication(self):

        self.login_user()

        # hace click en el boton para crear obra
        self.selenium.find_element_by_css_selector("#create_play").click()
        create_play_form = self.selenium.find_element_by_css_selector("#create_play_form")
        # Y por ultimo se aceptan los cambios
        create_play_form.find_element_by_css_selector('button[type="submit"]').click()

        errors = self.selenium.find_elements_by_css_selector(".alert-danger")
        errors = filter(lambda x: x.text != "", errors)
        list_errors = [
            u"Tiene que haber al menos una entrada",
            u"La obra tiene que tener un actor",
            u"This field is required.",
        ]

        for a in errors:
            self.assertTrue(a.is_displayed())
            self.assertTrue(a.text in list_errors)


class CreateProfileTestCase(BaseSeleniumTests):
    driver_type = "firefox"

    def _complete_profil_as(self, profile):
        profile_dict = {"owner_theater": "#select_theater",
                        "actor": "#select_actor", "spectator": "#select_spectator"}

        # hace click en el boton para crear perfil
        self.selenium.find_element_by_css_selector("#select_profile").click()

        self.selenium.find_element_by_css_selector(profile_dict.get(profile)).click()
        profile_form = self.selenium.find_element_by_css_selector("#create_profile_form")

        # completa con nombre de perfil
        name = "Juan"
        name_input = profile_form.find_element_by_css_selector("#id_name")
        name_input.clear()
        name_input.send_keys(name)

        # Apellido
        surname = "Topo"
        surname_input = profile_form.find_element_by_css_selector("#id_surname")
        surname_input.clear()
        surname_input.send_keys(surname)

        # facebook
        facebook = "Juan.Topo"
        facebook_input = profile_form.find_element_by_css_selector("#id_facebook")
        facebook_input.clear()
        facebook_input.send_keys(facebook)

        # twitter
        twitter = "Topo"
        twitter_input = profile_form.find_element_by_css_selector("#id_twitter")
        twitter_input.clear()
        twitter_input.send_keys(twitter)

        # Y una foto de perfil
        self.upload_image("#id_photo")
        # se aceptan los cambios
        profile_form.find_element_by_css_selector('button[type="submit"]').click()

        return name, surname, facebook, twitter

    def test_create_profile_as_owner_theater(self):

        user = self.login_user()
        name, surname, facebook, twitter = self._complete_profil_as("owner_theater")

        # Nos redirige a la pagina del perfil y se crear un perfil para el
        # usuario
        profile = OwnerTheater.objects.get(user=user)

        profile_url = "/profile/%s" % profile.id
        self.assertTrue(profile_url in self.selenium.current_url)
        self.assertEqual(profile.name, name)
        self.assertEqual(profile.surname, surname)
        self.assertEqual(profile.twitter, twitter)
        self.assertEqual(profile.facebook, facebook)

    def test_create_profile_as_actor(self):

        user = self.login_user()
        name, surname, facebook, twitter = self._complete_profil_as("actor")

        # Nos redirige a la pagina del perfil y se crear un perfil para el
        # usuario
        profile = Actor.objects.get(user=user)

        profile_url = "/profile/%s" % profile.id
        self.assertTrue(profile_url in self.selenium.current_url)
        self.assertEqual(profile.name, name)
        self.assertEqual(profile.surname, surname)
        self.assertEqual(profile.twitter, twitter)
        self.assertEqual(profile.facebook, facebook)

    def test_create_profile_as_spectator(self):

        user = self.login_user()
        name, surname, facebook, twitter = self._complete_profil_as("spectator")

        # Nos redirige a la pagina del perfil y se crear un perfil para el
        # usuario
        profile = Spectators.objects.get(user=user)

        profile_url = "/profile/%s" % profile.id
        self.assertTrue(profile_url in self.selenium.current_url)
        self.assertEqual(profile.name, name)
        self.assertEqual(profile.surname, surname)
        self.assertEqual(profile.twitter, twitter)
        self.assertEqual(profile.facebook, facebook)
