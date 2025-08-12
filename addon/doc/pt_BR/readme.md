# Links Favoritos

* **Autor**: Edilberto Fonseca ([edilberto.fonseca@outlook.com](mailto:edilberto.fonseca@outlook.com))
* **Data de Criação**: 11/04/2024
* **Licença**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Introdução

O add-on **FavoriteLinks** é uma ferramenta para gerenciar seus links favoritos de forma organizada e eficiente. Ele permite que você salve, edite e remova links em uma lista categorizada, oferecendo uma interface intuitiva com funcionalidades como adicionar novos links, renomear títulos, remover entradas indesejadas e gerenciar categorias.

Ao abrir o add-on, você tem acesso rápido aos seus links e pode abri-los diretamente no navegador padrão. Agora, também há suporte para a abertura de links em um navegador secundário, caso você precise de mais flexibilidade.

## Instalação

Siga os passos abaixo para instalar o add-on **FavoriteLinks** no NVDA:

1. No NVDA, abra o menu **Ferramentas** e selecione a **Loja de Complementos**.
2. Na guia **Complementos Disponíveis**, navegue até o campo **Procurar**.
3. Busque por "favoriteLinks". Nos resultados, pressione **Enter** ou **Aplicar** e, em seguida, escolha **Instalar**.
4. Reinicie o NVDA para aplicar as alterações.

## Configuração

Você tem controle total sobre o local onde seus links são salvos e sobre o navegador que os abre.

1. Acesse o menu do NVDA: `NVDA+N` > *Preferências* > *Configurações*.
2. Na lista de categorias, selecione **Links Favoritos**.

Você pode escolher um local personalizado para salvar o arquivo de links usando o botão **"Selecionar ou adicionar um diretório"** (`Alt+S`).

Para definir um navegador secundário, que pode ser tanto um instalado quanto um portátil:

1. Navegue com o `Tab` até o campo **Caminho do navegador**.
2. Use o botão **"Selecione o caminho do navegador"** (`Alt+N`) para adicionar o executável do navegador desejado.

## Uso

### Acessando o Add-on

* Pressione `Alt+Windows+K`.
* Ou acesse via `NVDA+N` > *Ferramentas* > *Links Favoritos*.

### Interface Principal

A interface principal é composta por dois campos principais, que podem ser navegados com a tecla `Tab`:

1. **Categoria**: Uma caixa de seleção com as categorias existentes.
2. **Lista de Links**: Uma lista que mostra os links associados à categoria selecionada.

Use o **menu de contexto** (tecla de aplicação) em qualquer um desses campos para acessar as opções adicionais.

### Ações Disponíveis

#### Na Caixa de Categorias

* **Adicionar Categoria**: Cria uma nova categoria.
* **Editar Categoria**: Renomeia a categoria selecionada.
* **Remover Categoria**: Exclui a categoria e todos os seus links.
* **Exportar Links**: Salva todos os links e categorias em um arquivo `.json`.
* **Importar Links**: Carrega links e categorias de um arquivo `.json`.

#### Na Lista de Links

* **Abrir Link**: Abre o link no navegador que você configurou.
    > **Observação**: É necessário configurar o navegador secundário previamente nas configurações.
* **Adicionar Link**: Permite inserir uma nova URL. O título será obtido automaticamente, mas você pode informá-lo manualmente caso a busca falhe.
* **Editar Link**: Modifica o título e a URL de um link existente.
* **Remover Link**: Exclui o link selecionado.
* **Exportar Links** / **Importar Links**: Igual às opções da categoria.
* **Ordenar Links**: Organiza os links da categoria atual em ordem alfabética.

### Atalhos

| Função | Atalho |
| :--- | :--- |
| Abrir Link | `Alt+B` ou `Enter` (na lista de links) |
| Adicionar Link | `Alt+A` |
| Adicionar Categoria | `Alt+D` |
| Editar Link | `Alt+E` ou `F2` |
| Excluir Link | `Alt+L` ou `Del` |
| Salvar URL da página atual | `Shift+Control+D` |
| Mostrar URL da página atual | `Windows+Control+P` Pressionando duas vezes, a URL é copiada para a área de transferência. |
| Sair | `Alt+S`, `Esc` ou `Alt+F4` |

## Diálogo "Adicionar Novo Link"

1. **Categoria**: Selecione a categoria desejada.
2. **URL**: Cole ou digite o endereço do link.
    > Se você já tiver copiado uma URL, ela será colada automaticamente.
3. **OK (`Alt+O`)**: Adiciona o link.
    > O título será buscado automaticamente. Caso a busca falhe, você poderá inseri-lo manualmente.
4. **Cancelar (`Alt+C`)**: Fecha o diálogo. `Esc` ou `Alt+F4` também funcionam.

## Diálogo "Editar Link"

1. **Categoria**: Ao alterar a categoria aqui, o link será movido para a nova categoria.
2. **Título**: Edite o título do link.
3. **URL**: Altere o endereço do link.
4. **OK (`Alt+O`)**: Salva as alterações.
5. **Cancelar (`Alt+C`)**: Fecha sem salvar. `Esc` ou `Alt+F4` também funcionam.

## Agradecimentos

Um agradecimento especial à **Rue Fontes** e ao **Ângelo Abrantes** pelos testes realizados e pelas sugestões valiosas que contribuíram significativamente para a melhoria deste projeto.

Agradeço também ao **Marlon Brandão de Sousa**, por compartilhar generosamente seu workflow, o que foi crucial para garantir a eficiência e qualidade do desenvolvimento.

O add-on FavoriteLinks foi desenvolvido com o auxílio do **ChatGPT** e do **Google Gemini**, usados para a criação de funções, otimização e refatoração do código, e para aprimorar a documentação.

## 🌍 Tradutores

* 🇸🇦 **Árabe** — Ahmed Bakr
* 🇧🇷 **Português (Brasil)** — Edilberto Fonseca
* 🇵🇹 **Português (Portugal)** — Edilberto Fonseca
* 🇷🇺 **Russo (Rússia)** — Valentin Kupriyanov
* 🇹🇷 **Turco (Turquia)** — Umut KORKMAZ
* 🇺🇦 **Ucraniano (Ucrânia)** — Heorhii Halas
