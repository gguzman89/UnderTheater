# vim: set fileencoding=utf-8 :
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.phantomjs.webdriver import WebDriver as PhatomWebDriver
from underTheaterApp.factories import PlayTheaterFactory


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



