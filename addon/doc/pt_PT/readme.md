# Ligações Favoritas

* **Autor**: Edilberto Fonseca ([edilberto.fonseca@outlook.com](mailto:edilberto.fonseca@outlook.com))
* **Data de Criação**: 11/04/2024
* **Licença**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Introdução

O add-on **FavoriteLinks** é uma ferramenta para gerir os seus links favoritos de forma organizada e eficiente. Permite guardar, editar e remover links numa lista categorizada, oferecendo uma interface intuitiva com funcionalidades como adicionar novos links, renomear títulos, remover entradas indesejadas e gerir categorias. Além disso, o add-on permite importar favoritos directamente de ficheiros HTML exportados pelos navegadores.

Ao abrir o add-on, tem acesso rápido aos seus links e pode abri-los directamente no navegador predefinido. Existe agora também suporte para abrir links num navegador secundário, caso necessite de maior flexibilidade.

## Instalação

Siga os passos abaixo para instalar o add-on **FavoriteLinks** no NVDA:

1. No NVDA, abra o menu **Ferramentas** e seleccione a **Loja de Complementos**.
2. No separador **Complementos Disponíveis**, navegue até ao campo **Procurar**.
3. Procure por "favoriteLinks". Nos resultados, prima **Enter** ou **Aplicar** e, de seguida, escolha **Instalar**.
4. Reinicie o NVDA para aplicar as alterações.

## Configuração

Tem controlo total sobre o local onde os seus links são guardados e sobre o navegador que os abre.

1. Aceda ao menu do NVDA: `NVDA+N` > *Preferências* > *Configurações*.
2. Na lista de categorias, seleccione **Links Favoritos**.

Pode escolher um local personalizado para guardar o ficheiro de links utilizando o botão **"Seleccionar ou adicionar um directório"** (`Alt+S`).

Para definir um navegador secundário, que pode ser tanto instalado como portátil:

1. Navegue com a tecla `Tab` até ao campo **Caminho do navegador**.
2. Utilize o botão **"Seleccionar o caminho do navegador"** (`Alt+N`) para adicionar o executável do navegador pretendido.

## Utilização

### Aceder ao Add-on

* Prima `Alt+Windows+K`.
* Ou aceda através de `NVDA+N` > *Ferramentas* > *Links Favoritos*.

### Interface Principal

A interface principal é composta por dois campos principais, que podem ser navegados com a tecla `Tab`:

1. **Categoria**: Uma caixa de selecção com as categorias existentes.
2. **Lista de Links**: Uma lista que mostra os links associados à categoria seleccionada.

Utilize o **menu de contexto** (tecla de aplicações) em qualquer um destes campos para aceder às opções adicionais.

### Acções Disponíveis

#### Na Caixa de Categorias

* **Adicionar Categoria**: Cria uma nova categoria.
* **Editar Categoria**: Renomeia a categoria seleccionada.
* **Remover Categoria**: Elimina a categoria e todos os seus links.
* **Exportar Links**: Guarda todos os links e categorias num ficheiro `.json`.
* **Importar Links**: Carrega links e categorias a partir de um ficheiro `.json`.

#### Na Lista de Links

* **Abrir Link**: Abre o link no navegador que configurou.
    > **Nota**: É necessário configurar previamente o navegador secundário nas configurações.
* **Adicionar Link**: Permite inserir um novo URL. O título será obtido automaticamente, mas pode introduzi-lo manualmente caso a obtenção falhe.
* **Editar Link**: Modifica o título e o URL de um link existente.
* **Remover Link**: Elimina o link seleccionado.
* **Exportar Links** / **Importar Links**: Iguais às opções da categoria.
* **Importar Favoritos de HTML**: Importa links a partir de um ficheiro `.html` exportado por navegadores.
* **Ordenar Links**: Organiza os links da categoria actual por ordem alfabética.

### Importar Favoritos de HTML

O FavoriteLinks também permite importar favoritos directamente de ficheiros HTML, como os exportados pelos navegadores (Chrome, Firefox, Edge, entre outros).

Esta funcionalidade é útil para migrar os seus favoritos existentes para o add-on de forma rápida e organizada.

#### Como importar favoritos a partir de um ficheiro HTML

1. Abra o add-on **Links Favoritos**.
2. Aceda ao menu de contexto na **Caixa de Categorias** ou utilize a opção disponível no menu principal.
3. Seleccione **Importar favoritos de HTML**.
4. Escolha o ficheiro `.html` exportado do seu navegador.
5. Aguarde o processamento dos links.

Durante a importação:

* O progresso é apresentado numa barra de progresso.
* Pode **cancelar a operação a qualquer momento**.
* O NVDA permanece responsivo durante todo o processo.

#### Organização dos links importados

* Os links importados são adicionados automaticamente ao ficheiro JSON configurado nas preferências do add-on.
* Por defeito, os favoritos são inseridos na categoria **“Imported Bookmarks”**.
* Links duplicados (com o mesmo URL) não são adicionados novamente.

No final da importação, é apresentada uma mensagem de confirmação e a interface do add-on é actualizada automaticamente.

### Atalhos

| Função | Atalho |
| :--- | :--- |
| Abrir Link | `Alt+B` ou `Enter` (na lista de links) |
| Adicionar Link | `Alt+A` |
| Adicionar Categoria | `Alt+D` |
| Editar Link | `Alt+E` ou `F2` |
| Eliminar Link | `Alt+L` ou `Del` |
| Guardar URL da página actual | `Shift+Control+D` |
| Mostrar URL da página actual | `Windows+Control+P` Ao pressionar duas vezes, o URL é copiado para a área de transferência. |
| Sair | `Alt+S`, `Esc` ou `Alt+F4` |

## Diálogo "Adicionar Novo Link"

1. **Categoria**: Seleccione a categoria pretendida.
2. **URL**: Cole ou escreva o endereço do link.
    > Se já tiver copiado um URL, este será colado automaticamente.
3. **OK (`Alt+O`)**: Adiciona o link.
    > O título será obtido automaticamente. Caso a obtenção falhe, poderá introduzi-lo manualmente.
4. **Cancelar (`Alt+C`)**: Fecha o diálogo. `Esc` ou `Alt+F4` também funcionam.

## Diálogo "Editar Link"

1. **Categoria**: Ao alterar a categoria aqui, o link será movido para a nova categoria.
2. **Título**: Edite o título do link.
3. **URL**: Altere o endereço do link.
4. **OK (`Alt+O`)**: Guarda as alterações.
5. **Cancelar (`Alt+C`)**: Fecha sem guardar. `Esc` ou `Alt+F4` também funcionam.

## Agradecimentos

Um agradecimento especial à **Rue Fontes** e ao **Ângelo Abrantes** pelos testes realizados e pelas sugestões valiosas que contribuíram significativamente para a melhoria deste projecto.

Agradeço também ao **Abel Passos** pela contribuição com a funcionalidade de importação de favoritos a partir de ficheiros HTML.

O add-on FavoriteLinks foi desenvolvido com o auxílio do **ChatGPT** e do **Google Gemini**, utilizados para a criação de funções, optimização e refactorização do código, bem como para a melhoria da documentação.

## 🌍 Tradutores

* 🇸🇦 **Árabe** — Ahmed Bakr
* 🇧🇷 **Português (Brasil)** — Edilberto Fonseca
* 🇵🇹 **Português (Portugal)** — Edilberto Fonseca
* 🇷🇺 **Russo (Rússia)** — Valentin Kupriyanov
* 🇹🇷 **Turco (Turquia)** — Umut KORKMAZ
* 🇺🇦 **Ucraniano (Ucrânia)** — Heorhii Halas
