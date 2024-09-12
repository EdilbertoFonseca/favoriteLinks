# Links Favoritos

* **Autor**: Edilberto Fonseca <edilberto.fonseca@outlook.com>
* **Data de Criação**: 11/04/2024
* **Licença**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Introdução

O add-on **FavoriteLinks** é uma ferramenta que permite gerir links favoritos de forma organizada e eficiente. Com ele, pode guardar, editar e remover links numa lista categorizada. A sua interface intuitiva oferece funcionalidades abrangentes, como adicionar novos links, editar títulos, remover links indesejados e gerir categorias. Ao abrir o add-on, tem acesso rápido aos seus links favoritos e pode abrir um link seleccionado directamente no navegador.

> Observação: O add-on FavoriteLinks foi desenvolvido com o auxílio do ChatGPT para criar algumas funções, optimizar o desempenho e organizar o código.

## Instalação

Siga as instruções abaixo para instalar o add-on Favorite Links no NVDA:

1. **Descarregue o ficheiro de instalação do add-on**: Obtenha o ficheiro na Loja de Complementos do NVDA.
   **Nota**: Se o add-on for descarregado da loja, a instalação ocorrerá automaticamente. Caso contrário, siga as instruções abaixo.
2. **Instale o add-on**: Pressione Enter sobre o ficheiro do add-on descarregado.
3. **Siga as instruções no ecrã**: Complete a instalação conforme as orientações fornecidas.
4. **Reinicie o NVDA**: É necessário reiniciar para activar o add-on.
5. **Verifique a instalação**: Pressione `NVDA+N` para abrir o menu do NVDA, vá a "Ferramentas" e verifique se o Favorite Links está listado.

## Configuração

Pode seleccionar um local diferente do padrão para guardar o seu ficheiro de links. Para isso, basta aceder ao menu do NVDA, ir a Preferências, Configurações e, em Configurações, seleccionar a categoria Links Favoritos. Em seguida, escolha uma pasta diferente utilizando o botão “Seleccione ou adicione um directório”.

## Uso

### Aceder ao Add-on

Pressione `alt+windows+K` ou use o menu do NVDA `NVDA+N` > Ferramentas > Links Favoritos para abrir o complemento.

### Interface Principal

O diálogo exibido terá dois campos principais:

1. **Categoria**: Uma caixa de selecção onde pode escolher a categoria desejada.
2. **Lista de Links**: Aqui, os links correspondentes à categoria seleccionada serão exibidos.

### Acções Disponíveis

Para aceder às opções para trabalhar com os links e categorias, pode usar o menu de Contexto (tecla de aplicação) do NVDA.

### Categoria

Estando posicionado na caixa de combinação das categorias, as seguintes opções são exibidas:

* **Adicionar categoria**: Permite adicionar uma categoria à lista.
* **Editar Categoria**: Permite renomear uma categoria existente.
* **Remover Categoria**: Permite excluir uma categoria e todos os links associados a ela.
* **Exportar links**: Permite exportar os links e categorias guardados no ficheiro json.
* **Importar links**: Permite importar os links e categorias guardados anteriormente para o ficheiro json.

### Lista de Links

Estando posicionado na lista de links, as seguintes opções são exibidas:

* **Abrir Link**: Abre o link seleccionado no navegador padrão do sistema.
  > Observação: Pressionando Enter sobre o link seleccionado, este é aberto no navegador padrão do sistema.
* **Adicionar Link**: Permite adicionar um novo link informando a sua URL e categoria.
  > Observação: O título é obtido automaticamente. Quando o título não puder ser obtido, será exibido um diálogo para que adicione o título manualmente.
* **Editar Link**: Permite editar o título de um link existente e a sua URL.
* **Remover Link**: Permite remover um link da lista.
* **Exportar links**: Permite exportar os links e categorias guardados no ficheiro json.
* **Importar links**: Permite importar os links e categorias guardados anteriormente para o ficheiro json.
* **Ordenar Links**: Permite ordenar os links por ordem alfabética.

### Atalhos

Algumas opções estão disponíveis através de atalhos directos na interface. São elas:

* **Abrir link, `alt+B`**: Abre o link seleccionado no navegador padrão do sistema.
  > Observação: Pressionando Enter sobre o link seleccionado, este é aberto no navegador padrão do sistema.
* **Adicionar link, `alt+A`**: Permite adicionar um novo link informando a sua URL e categoria.
  > Observação: O título é obtido automaticamente. Quando o título não puder ser obtido, será exibido um diálogo para que adicione o título manualmente.
* **Editar link, `alt+E`**: Permite editar o título de um link existente e a sua URL.
* **Eliminar link, `alt+L`**: Permite remover um link da lista.
* **Adicionar categoria, `alt+D`**: Permite adicionar uma categoria à lista.
* **Sair, `alt+S`**: Encerra o diálogo. Pode também usar a tecla "Escape" ou Alt+F4.

## Diálogo Adicionar Novo Link

1. **Categoria**: Uma caixa de selecção onde pode escolher a categoria desejada.
2. **Campo para adição da URL do link**: Uma caixa de texto onde pode colar a URL.
   > Observação: Caso já tenha copiado a URL, esta será colocada automaticamente na caixa de edição.
3. **OK, `alt+O`**: Adiciona o link na lista.
   > Observação: O título é obtido automaticamente. Quando o título não puder ser obtido, será exibido um diálogo para que adicione o título manualmente.
4. **Cancelar, `alt+C`**: Encerra o diálogo. Pode também usar a tecla "Escape" ou Alt+F4.

## Diálogo Editar link

1. **Categoria**: Uma caixa de seleção onde podes escolher a categoria desejada.
   > Ao selecionar outra categoria, o link será guardado na nova categoria selecionada.
2. **Campo para edição do título do URL**: Uma caixa de texto onde podes editar o título associado ao URL.
3. **Campo para edição do URL**: Uma caixa de texto onde podes editar o URL.
4. **OK, `Alt+O`**: Guarda as modificações realizadas.
5. **Cancelar, `Alt+C`**: Encerra o diálogo. Também podes usar a tecla "Escape" ou "Alt+F4".

## Agradecimentos

Agradeço a Rue Fontes e Ângelo Abrantes pelos testes e sugestões para melhoria deste projecto, e a Marlon Brandão de Sousa por partilhar generosamente o seu workflow, que foi crucial para a eficiência e qualidade do projecto.

### Tradutores

* **árabe** por Ahmed Bakr.
* **português (Brasil)** por Edilberto Fonseca.
* **turco (Turquia)** por Umut KORKMAZ.
* **ucraniano (Ucrânia)** por Heorhii Halas.
