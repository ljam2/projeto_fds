from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager

class FunctionalTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Rodar sem interface gráfica
        # Corrigindo a inicialização do ChromeDriver
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="130.0.6723.70").install()), options=chrome_options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_fornecedor_cadastrar_produto(self):
        # Faz login como fornecedor
        self.driver.get(f'{self.live_server_url}/login/')
        username_input = self.driver.find_element(By.NAME, 'nome_usuario')
        password_input = self.driver.find_element(By.NAME, 'senha')
        username_input.send_keys('fornecedor_teste')
        password_input.send_keys('senha_teste')
        password_input.send_keys(Keys.RETURN)
        
        # Espera explícita até a página de redirecionamento
        WebDriverWait(self.driver, 10).until(EC.url_contains('/home_fornecedor'))

        # Acessa a página de cadastro de produto
        self.driver.get(f'{self.live_server_url}/cadastrar_produto/')
        
        # Preenche os campos obrigatórios do formulário
        nome_produto = self.driver.find_element(By.NAME, 'nome_produto')
        descricao = self.driver.find_element(By.NAME, 'descricao')
        preco = self.driver.find_element(By.NAME, 'preco')
        estoque = self.driver.find_element(By.NAME, 'estoque')
        disponivel = self.driver.find_element(By.NAME, 'disponivel')

        nome_produto.send_keys('Produto Teste')
        descricao.send_keys('Descrição do produto teste')
        preco.send_keys('50.00')
        estoque.send_keys('20')
        disponivel.click()
        
        # Envia o formulário
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Espera pelo redirecionamento
        WebDriverWait(self.driver, 10).until(EC.url_contains('/home_fornecedor'))

        # Verifica se o produto foi cadastrado e está listado na página do fornecedor
        page_source = self.driver.page_source
        self.assertIn('Produto Teste', page_source)

    def test_cliente_revisar_e_editar_carrinho(self):
        # Faz login como cliente
        self.driver.get(f'{self.live_server_url}/login/')
        username_input = self.driver.find_element(By.NAME, 'nome_usuario')
        password_input = self.driver.find_element(By.NAME, 'senha')
        username_input.send_keys('cliente_teste')
        password_input.send_keys('senha_teste')
        password_input.send_keys(Keys.RETURN)
        
        WebDriverWait(self.driver, 10).until(EC.url_contains('/home'))

        # Acessa a página de exibir carrinho
        self.driver.get(f'{self.live_server_url}/carrinho/')
        
        # Verifica se há itens no carrinho
        page_source = self.driver.page_source
        self.assertIn('Seu carrinho', page_source)
        
        # Edita a quantidade de um item no carrinho
        quantidade_input = self.driver.find_element(By.NAME, 'quantidade')
        quantidade_input.clear()
        quantidade_input.send_keys('2')
        
        # Envia a alteração
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Verifica se o carrinho foi atualizado com a nova quantidade
        total = self.driver.find_element(By.ID, 'total_carrinho').text
        self.assertIn('Total atualizado', total)

    def test_fornecedor_historico_vendas(self):
        # Faz login como fornecedor
        self.driver.get(f'{self.live_server_url}/login/')
        username_input = self.driver.find_element(By.NAME, 'nome_usuario')
        password_input = self.driver.find_element(By.NAME, 'senha')
        username_input.send_keys('fornecedor_teste')
        password_input.send_keys('senha_teste')
        password_input.send_keys(Keys.RETURN)
        
        WebDriverWait(self.driver, 10).until(EC.url_contains('/home_fornecedor'))

        # Acessa o histórico de vendas
        self.driver.get(f'{self.live_server_url}/historico_vendas/')

        # Verifica se o histórico de vendas contém vendas
        page_source = self.driver.page_source
        self.assertIn('Histórico de Vendas', page_source)
        self.assertIn('Produto Teste', page_source)

    def test_cliente_historico_compras(self):
        # Faz login como cliente
        self.driver.get(f'{self.live_server_url}/login/')
        username_input = self.driver.find_element(By.NAME, 'nome_usuario')
        password_input = self.driver.find_element(By.NAME, 'senha')
        username_input.send_keys('cliente_teste')
        password_input.send_keys('senha_teste')
        password_input.send_keys(Keys.RETURN)
        
        WebDriverWait(self.driver, 10).until(EC.url_contains('/home'))

        # Acessa o histórico de compras
        self.driver.get(f'{self.live_server_url}/historico_compras/')

        # Verifica se o histórico de compras contém compras
        page_source = self.driver.page_source
        self.assertIn('Histórico de Compras', page_source)

    def test_cliente_adicionar_itens_ao_carrinho(self):
        # Faz login como cliente
        self.driver.get(f'{self.live_server_url}/login/')
        username_input = self.driver.find_element(By.NAME, 'nome_usuario')
        password_input = self.driver.find_element(By.NAME, 'senha')
        username_input.send_keys('cliente_teste')
        password_input.send_keys('senha_teste')
        password_input.send_keys(Keys.RETURN)
        
        WebDriverWait(self.driver, 10).until(EC.url_contains('/home'))

        # Acessa a página de um produto
        self.driver.get(f'{self.live_server_url}/detalhes_anonimo/1/')  # Produto ID 1

        # Adiciona o produto ao carrinho
        self.driver.find_element(By.XPATH, '//button[text()="Adicionar ao carrinho"]').click()

        WebDriverWait(self.driver, 10).until(EC.url_contains('/carrinho'))

        # Verifica se o produto foi adicionado ao carrinho
        page_source = self.driver.page_source
        self.assertIn('Produto Teste', page_source)

    def test_cliente_favoritar_produto(self):
        # Faz login como cliente
        self.driver.get(f'{self.live_server_url}/login/')
        username_input = self.driver.find_element(By.NAME, 'nome_usuario')
        password_input = self.driver.find_element(By.NAME, 'senha')
        username_input.send_keys('cliente_teste')
        password_input.send_keys('senha_teste')
        password_input.send_keys(Keys.RETURN)
        
        WebDriverWait(self.driver, 10).until(EC.url_contains('/home'))

        # Acessa a página de um produto
        self.driver.get(f'{self.live_server_url}/detalhes/1/')  # Produto ID 1

        # Favorita o produto
        self.driver.find_element(By.XPATH, '//button[text()="Favoritar"]').click()

        WebDriverWait(self.driver, 10).until(EC.url_contains('/favoritos'))

        # Verifica se o produto foi favoritado
        page_source = self.driver.page_source
        self.assertIn('Produto Teste', page_source)
