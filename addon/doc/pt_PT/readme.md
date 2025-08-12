# Ligações Favoritas

* **Autor**: Edilberto Fonseca ([edilberto.fonseca@outlook.com](mailto:edilberto.fonseca@outlook.com))
* **Data de Criação**: 11/04/2024
* **Licença**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Introdução

O add-on **FavoriteLinks** é uma ferramenta para gerir os teus links favoritos de forma organizada e eficiente. Permite-te guardar, editar e remover links numa lista categorizada, oferecendo uma interface intuitiva com funcionalidades como adicionar novos links, renomear títulos, remover entradas indesejadas e gerir categorias.

Ao abrir o add-on, tens acesso rápido aos teus links e podes abri-los diretamente no navegador predefinido. Agora, também há suporte para abrir links num navegador secundário, caso precises de mais flexibilidade.

## Instalação

Segue os passos abaixo para instalar o add-on **FavoriteLinks** no NVDA:

1. No NVDA, abre o menu **Ferramentas** e seleciona a **Loja de Extras**.
2. No separador **Extras Disponíveis**, navega até ao campo **Procurar**.
3. Procura por "favoriteLinks". Nos resultados, prime **Enter** ou **Aplicar** e, em seguida, escolhe **Instalar**.
4. Reinicia o NVDA para aplicar as alterações.

## Configuração

Tens controlo total sobre o local onde os teus links são guardados e sobre o navegador que os abre.

1. Acede ao menu do NVDA: `NVDA+N` > *Preferências* > *Definições*.
2. Na lista de categorias, seleciona **Links Favoritos**.

Podes escolher um local personalizado para guardar o ficheiro de links usando o botão **"Selecionar ou adicionar um diretório"** (`Alt+S`).

Para definires um navegador secundário, que pode ser tanto instalado como portátil:

1. Navega com o `Tab` até ao campo **Caminho do navegador**.
2. Usa o botão **"Selecionar o caminho do navegador"** (`Alt+N`) para adicionar o executável do navegador pretendido.

## Utilização

### Aceder ao Add-on

* Prime `Alt+Windows+K`.
* Ou acede via `NVDA+N` > *Ferramentas* > *Links Favoritos*.

### Interface Principal

A interface principal é composta por dois campos principais, que podem ser navegados com a tecla `Tab`:

1. **Categoria**: Uma caixa de seleção com as categorias existentes.
2. **Lista de Links**: Uma lista que mostra os links associados à categoria selecionada.

Utiliza o **menu de contexto** (tecla de aplicação) em qualquer um destes campos para aceder às opções adicionais.

### Ações Disponíveis

#### Na Caixa de Categorias

* **Adicionar Categoria**: Cria uma nova categoria.
* **Editar Categoria**: Renomeia a categoria selecionada.
* **Remover Categoria**: Exclui a categoria e todos os seus links.
* **Exportar Links**: Guarda todos os links e categorias num ficheiro `.json`.
* **Importar Links**: Carrega links e categorias a partir de um ficheiro `.json`.

#### Na Lista de Links

* **Abrir Link**: Abre o link no navegador que configuraste.
    > **Nota**: É necessário configurar previamente o navegador secundário nas definições.
* **Adicionar Link**: Permite inserir um novo URL. O título será obtido automaticamente, mas podes indicá-lo manualmente caso a pesquisa falhe.
* **Editar Link**: Modifica o título e o URL de um link existente.
* **Remover Link**: Elimina o link selecionado.
* **Exportar Links** / **Importar Links**: Igual às opções da categoria.
* **Ordenar Links**: Organiza os links da categoria atual por ordem alfabética.

### Atalhos

| Função | Atalho |
| :--- | :--- |
| Abrir Link | `Alt+B` ou `Enter` (na lista de links) |
| Adicionar Link | `Alt+A` |
| Adicionar Categoria | `Alt+D` |
| Editar Link | `Alt+E` ou `F2` |
| Eliminar Link | `Alt+L` ou `Del` |
| Guardar URL da página atual | `Shift+Control+D` |
| Mostrar URL da página atual | `Windows+Control+P` Pressionando duas vezes, a URL é copiada para a área de transferência. |
| Sair | `Alt+S`, `Esc` ou `Alt+F4` |

## Diálogo "Adicionar Novo Link"

1. **Categoria**: Seleciona a categoria desejada.
2. **URL**: Cola ou digita o endereço do link.
    > Se já tiveres copiado um URL, este será colado automaticamente.
3. **OK (`Alt+O`)**: Adiciona o link.
    > O título será procurado automaticamente. Caso a pesquisa falhe, poderás inseri-lo manualmente.
4. **Cancelar (`Alt+C`)**: Fecha o diálogo. `Esc` ou `Alt+F4` também funcionam.

## Diálogo "Editar Link"

1. **Categoria**: Ao alterar a categoria aqui, o link será movido para a nova categoria.
2. **Título**: Edita o título do link.
3. **URL**: Altera o endereço do link.
4. **OK (`Alt+O`)**: Guarda as alterações.
5. **Cancelar (`Alt+C`)**: Fecha sem guardar. `Esc` ou `Alt+F4` também funcionam.

## Agradecimentos

Um agradecimento especial à **Rue Fontes** e ao **Ângelo Abrantes** pelos testes realizados e pelas sugestões valiosas que contribuíram significativamente para a melhoria deste projeto.

Agradeço também ao **Marlon Brandão de Sousa**, por partilhar generosamente o seu workflow, o que foi crucial para garantir a eficiência e qualidade do desenvolvimento.

O add-on FavoriteLinks foi desenvolvido com o auxílio do **ChatGPT** e do **Google Gemini**, utilizados para a criação de funções, optimização e refatoração do código, e para melhorar a documentação.

## 🌍 Tradutores

* 🇸🇦 **Árabe** — Ahmed Bakr  
* 🇧🇷 **Português (Brasil)** — Edilberto Fonseca  
* 🇵🇹 **Português (Portugal)** — Edilberto Fonseca  
* 🇷🇺 **Russo (Rússia)** — Valentin Kupriyanov  
* 🇹🇷 **Turco (Turquia)** — Umut KORKMAZ  
* 🇺🇦 **Ucraniano (Ucrânia)** — Heorhii Halas
