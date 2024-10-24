from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager

class FunctionalTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Rodar sem interface gráfica
        # Corrigindo a inicialização do ChromeDriver
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_fornecedor_cadastrar_produto(self):
        # Faz login como fornecedor
        self.driver.get(f'{self.live_server_url}/login/')
        username_input = self.driver.find_element_by_name('nome_usuario')
        password_input = self.driver.find_element_by_name('senha')
        username_input.send_keys('fornecedor_teste')
        password_input.send_keys('senha_teste')
        password_input.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Aguardar o login

        # Acessa a página de cadastro de produto
        self.driver.get(f'{self.live_server_url}/cadastrar_produto/')
        
        # Preenche os campos obrigatórios do formulário
        nome_produto = self.driver.find_element_by_name('nome_produto')
        descricao = self.driver.find_element_by_name('descricao')
        preco = self.driver.find_element_by_name('preco')
        estoque = self.driver.find_element_by_name('estoque')
        disponivel = self.driver.find_element_by_name('disponivel')

        nome_produto.send_keys('Produto Teste')
        descricao.send_keys('Descrição do produto teste')
        preco.send_keys('50.00')
        estoque.send_keys('20')
        disponivel.click()
        
        # Envia o formulário
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()

        time.sleep(2)  # Aguardar o redirecionamento

        # Verifica se o produto foi cadastrado e está listado na página do fornecedor
        self.driver.get(f'{self.live_server_url}/home_fornecedor/')
        page_source = self.driver.page_source
        self.assertIn('Produto Teste', page_source)

    def test_cliente_revisar_e_editar_carrinho(self):
        # Faz login como cliente
        self.driver.get(f'{self.live_server_url}/login/')
        username_input = self.driver.find_element_by_name('nome_usuario')
        password_input = self.driver.find_element_by_name('senha')
        username_input.send_keys('cliente_teste')
        password_input.send_keys('senha_teste')
        password_input.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Aguardar o login

        # Acessa a página de exibir carrinho
        self.driver.get(f'{self.live_server_url}/carrinho/')
        
        # Verifica se há itens no carrinho
        page_source = self.driver.page_source
        self.assertIn('Seu carrinho', page_source)
        
        # Edita a quantidade de um item no carrinho
        quantidade_input = self.driver.find_element_by_name('quantidade')
        quantidade_input.clear()
        quantidade_input.send_keys('2')
        
        # Envia a alteração
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()

        time.sleep(2)  # Aguardar atualização

        # Verifica se o carrinho foi atualizado com a nova quantidade
        total = self.driver.find_element_by_id('total_carrinho').text
        self.assertIn('Total atualizado', total)

    def test_fornecedor_historico_vendas(self):
        # Faz login como fornecedor
        self.driver.get(f'{self.live_server_url}/login/')
        username_input = self.driver.find_element_by_name('nome_usuario')
        password_input = self.driver.find_element_by_name('senha')
        username_input.send_keys('fornecedor_teste')
        password_input.send_keys('senha_teste')
        password_input.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Aguardar o login

        # Acessa o histórico de vendas
        self.driver.get(f'{self.live_server_url}/historico_vendas/')

        # Verifica se o histórico de vendas contém vendas
        page_source = self.driver.page_source
        self.assertIn('Histórico de Vendas', page_source)
        self.assertIn('Produto Teste', page_source)

    def test_cliente_historico_compras(self):
        # Faz login como cliente
        self.driver.get(f'{self.live_server_url}/login/')
        username_input = self.driver.find_element_by_name('nome_usuario')
        password_input = self.driver.find_element_by_name('senha')
        username_input.send_keys('cliente_teste')
        password_input.send_keys('senha_teste')
        password_input.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Aguardar o login

        # Acessa o histórico de compras
        self.driver.get(f'{self.live_server_url}/historico_compras/')

        # Verifica se o histórico de compras contém compras
        page_source = self.driver.page_source
        self.assertIn('Histórico de Compras', page_source)

    def test_cliente_adicionar_itens_ao_carrinho(self):
        # Faz login como cliente
        self.driver.get(f'{self.live_server_url}/login/')
        username_input = self.driver.find_element_by_name('nome_usuario')
        password_input = self.driver.find_element_by_name('senha')
        username_input.send_keys('cliente_teste')
        password_input.send_keys('senha_teste')
        password_input.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Aguardar o login

        # Acessa a página de um produto
        self.driver.get(f'{self.live_server_url}/detalhes_anonimo/1/')  # Produto ID 1

        # Adiciona o produto ao carrinho
        self.driver.find_element_by_xpath('//button[text()="Adicionar ao carrinho"]').click()

        time.sleep(2)  # Aguardar a ação

        # Verifica se o produto foi adicionado ao carrinho
        self.driver.get(f'{self.live_server_url}/carrinho/')
        page_source = self.driver.page_source
        self.assertIn('Produto Teste', page_source)

    def test_cliente_favoritar_produto(self):
        # Faz login como cliente
        self.driver.get(f'{self.live_server_url}/login/')
        username_input = self.driver.find_element_by_name('nome_usuario')
        password_input = self.driver.find_element_by_name('senha')
        username_input.send_keys('cliente_teste')
        password_input.send_keys('senha_teste')
        password_input.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Aguardar o login

        # Acessa a página de um produto
        self.driver.get(f'{self.live_server_url}/detalhes/1/')  # Produto ID 1

        # Favorita o produto
        self.driver.find_element_by_xpath('//button[text()="Favoritar"]').click()

        time.sleep(2)  # Aguardar a ação

        # Verifica se o produto foi favoritado
        self.driver.get(f'{self.live_server_url}/favoritos/')
        page_source = self.driver.page_source
        self.assertIn('Produto Teste', page_source)
