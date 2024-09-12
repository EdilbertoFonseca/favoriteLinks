# Links Favoritos

* **Autor**: Edilberto Fonseca <edilberto.fonseca@outlook.com>
* **Data de Criação**: 11/04/2024
* **Licença**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Introdução

O add-on **FavoriteLinks** é uma ferramenta que permite gerenciar links favoritos de forma organizada e eficiente. Com ele, você pode salvar, editar e remover links em uma lista categorizada. Sua interface intuitiva oferece funcionalidades abrangentes, como adicionar novos links, editar títulos, remover links indesejados e gerenciar categorias. Ao abrir o add-on, você tem acesso rápido aos seus links favoritos e pode abrir um link selecionado diretamente no navegador.

> Observação: O add-on FavoriteLinks foi desenvolvido com o auxílio do ChatGPT para criação de algumas funções e otimização, ele também foi usado para a organização do código.

## Instalação

Siga as instruções abaixo para instalar o add-on Favorite Links no NVDA:

1. **Baixe o arquivo de instalação do add-on**: Obtenha o arquivo da Loja de Complementos do NVDA.
   **Nota**: Se o add-on for baixado da loja, a instalação ocorrerá automaticamente. Caso contrário, siga as instruções abaixo.
2. **Instale o add-on**: Pressione Enter sobre o arquivo do add-on baixado.
3. **Siga as instruções na tela**: Complete a instalação conforme as orientações fornecidas.
4. **Reinicie o NVDA**: É necessário reiniciar para ativar o add-on.
5. **Verifique a instalação**: Pressione `NVDA+N` para abrir o menu do NVDA, vá até "Ferramentas" e verifique se o Favorite Links está listado.

## Configuração

Você pode selecionar um local diferente do padrão para salvar seu arquivo de links. Para isso, basta acessar o menu do NVDA, ir a Preferências, Configurações e, em Configurações, selecionar a categoria Links Favoritos. Em seguida, escolha uma pasta diferente usando o botão “Selecione ou adicione um diretório”.

## Uso

### Acessando o Add-on

Pressione `Alt+Windows+K` ou use o menu do NVDA `NVDA+N` > Ferramentas > Links Favoritos para abrir o complemento.

### Interface Principal

O diálogo exibido terá dois campos principais:

1. **Categoria**: Uma caixa de seleção onde você pode escolher a categoria desejada.
2. **Lista de Links**: Aqui, os links correspondentes à categoria selecionada serão exibidos.

### Ações Disponíveis

Para ter acesso às opções para trabalhar com os links e categorias, você pode usar o menu de Contexto (tecla de aplicação) do NVDA.

### Categoria

Estando posicionado na caixa de combinação das categorias, as seguintes opções são exibidas:

* **Adicionar categoria**: Permite a adição de uma categoria à lista.
* **Editar Categoria**: Permite renomear uma categoria existente.
* **Remover Categoria**: Permite excluir uma categoria e todos os links associados a ela.
* **Exportar links**: Permite a exportação dos links e categorias salvos no arquivo json.
* **Importar links**: Permite a importação dos links e categorias salvos anteriormente para o arquivo json.

### Lista de Links

Estando posicionado na lista de links, as seguintes opções são exibidas:

* **Abrir Link**: Abre o link selecionado no navegador padrão do sistema. **Observação**: Pressionando Enter sobre o link selecionado, o mesmo é aberto no navegador padrão do sistema.
* **Adicionar Link**: Permite adicionar um novo link informando sua URL e categoria.
  > **Observação**: O título é obtido automaticamente. Quando o título não puder ser obtido, será exibido um diálogo para que você adicione o título manualmente.
* **Editar Link**: Permite editar o título de um link existente e sua URL.
* **Remover Link**: Permite remover um link da lista.
* **Exportar links**: Permite a exportação dos links e categorias salvos no arquivo json.
* **Importar links**: Permite a importação dos links e categorias salvos anteriormente para o arquivo json.
* **Ordenar Links**: Permite ordenar os links em ordem alfabética.

### Atalhos

Algumas opções estão disponíveis através de atalhos diretos na interface. São elas:

* **Abrir link, `alt+B`**: Abre o link selecionado no navegador padrão do sistema.
   > **Observação**: Pressionando Enter sobre o link selecionado, o mesmo é aberto no navegador padrão do sistema.
* **Adicionar link, `alt+A`**: Permite adicionar um novo link informando sua URL e categoria.
   > **Observação**: O título é obtido automaticamente. Quando o título não puder ser obtido, será exibido um diálogo para que você adicione o título manualmente.
* **Editar link, `alt+E`**: Permite editar o título de um link existente e sua URL.
* **Excluir link, `alt+L`**: Permite remover um link da lista.
* **Adicionar categoria, `alt+D`**: Permite a adição de uma categoria à lista.
* **Sair, `alt+S`**: Encerra o diálogo. Você também pode usar a tecla "Escape" ou Alt+F4.

## Diálogo Adicionar Novo Link

1. **Categoria**: Uma caixa de seleção onde você pode escolher a categoria desejada.
2. **Campo para adição da URL do link**: Uma caixa de texto onde você pode colar a URL.
   > **Observação**: Caso já tenha copiado a URL, ela será colocada automaticamente na caixa de edição.
3. **OK, `alt+O`**: Adiciona o link na lista.
   > **Observação**: O título é obtido automaticamente. Quando o título não puder ser obtido, será exibido um diálogo para que você adicione o título manualmente.
4. **Cancelar, `alt+C`**: Encerra o diálogo. Você também pode usar a tecla "Escape" ou Alt+F4.

## Diálogo Editar link

1. **Categoria**: Uma caixa de seleção onde você pode escolher a categoria desejada.
   > Ao selecionar outra categoria, o link será salvo na nova categoria selecionada.
2. **Campo para edição do título do URL**: Uma caixa de texto onde você pode editar o título associado ao URL.
3. **Campo para edição da URL**: Uma caixa de texto onde você pode editar o URL.
4. **OK, `Alt+O`**: Salva as modificações realizadas.
5. **Cancelar, `Alt+C`**: Encerra o diálogo. Você também pode usar a tecla "Escape" ou "Alt+F4".

## Agradecimentos

Agradeço a Rue Fontes e Ângelo Abrantes pelos testes e dicas para melhoria deste projeto, e a Marlon Brandão de Sousa por compartilhar generosamente seu workflow, que foi crucial para a eficiência e qualidade do projeto.

### Tradutores

* **árabe** por Ahmed Bakr.
* **português (Brasil)** por Edilberto Fonseca.
* **turco (Turquia)** por Umut KORKMAZ.
* **ucraniano (Ucrânia)** por Heorhii Halas.
