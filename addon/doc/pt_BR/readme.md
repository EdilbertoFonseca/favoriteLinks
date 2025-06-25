# Links Favoritos

* **Autor**: Edilberto Fonseca ([edilberto.fonseca@outlook.com](mailto:edilberto.fonseca@outlook.com))
* **Data de Criação**: 11/04/2024
* **Licença**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## 📌 Introdução

O add-on **FavoriteLinks** é uma ferramenta que permite gerenciar links favoritos de forma organizada e eficiente. Com ele, você pode salvar, editar e remover links em uma lista categorizada. Sua interface intuitiva oferece funcionalidades completas, como adicionar novos links, editar títulos, remover entradas indesejadas e gerenciar categorias.

Ao abrir o add-on, você tem acesso rápido aos seus links favoritos e pode abrir qualquer link selecionado diretamente no navegador padrão.

> **Observação**: O add-on FavoriteLinks foi desenvolvido com o auxílio do ChatGPT, usado tanto para a criação de algumas funções quanto para a organização e otimização do código.

## 💾 Instalação

Siga os passos abaixo para instalar o add-on **FavoriteLinks** no NVDA:

1. **Baixe o arquivo de instalação**: Você pode obtê-lo na Loja de Complementos do NVDA.

   > **Nota**: Se o add-on for baixado da loja, a instalação será automática. Caso contrário, siga os próximos passos.

2. **Instale o add-on**: Pressione `Enter` sobre o arquivo `.nvda-addon` baixado.

3. **Siga as instruções na tela**: Conclua a instalação conforme indicado.

4. **Reinicie o NVDA**: É necessário reiniciar para ativar o complemento.

5. **Verifique a instalação**: Pressione `NVDA+N`, vá até *Ferramentas* e verifique se **Links Favoritos** está listado.

## ⚙️ Configuração

Você pode escolher um local personalizado para salvar o arquivo de links. Para isso:

1. Acesse o menu do NVDA: `NVDA+N` > *Preferências* > *Configurações*.
2. Na lista de categorias, selecione **Links Favoritos**.
3. Use o botão **"Selecionar ou adicionar um diretório"** para definir a nova pasta de salvamento.

## 🚀 Uso

### Acessando o Add-on

* Pressione `Alt+Windows+K`, ou
* Acesse via `NVDA+N` > *Ferramentas* > *Links Favoritos*.

### Interface Principal

A interface principal possui dois campos principais:

1. **Categoria**: Caixa de seleção com as categorias existentes.
2. **Lista de Links**: Mostra os links associados à categoria selecionada.

### Ações Disponíveis

Use o **menu de contexto** (tecla de aplicação) enquanto estiver focado em uma das listas para acessar opções adicionais.

#### Categoria

Na caixa de combinação de categorias, estão disponíveis:

* **Adicionar Categoria**: Cria uma nova categoria.
* **Editar Categoria**: Renomeia a categoria selecionada.
* **Remover Categoria**: Exclui a categoria e seus links.
* **Exportar Links**: Salva os links e categorias em um arquivo `.json`.
* **Importar Links**: Carrega links e categorias de um arquivo `.json`.

#### Lista de Links

Na lista de links, estão disponíveis:

* **Abrir Link**: Abre o link no navegador padrão.

  > Pressionar `Enter` também abre o link.

* **Adicionar Link**: Permite inserir uma nova URL e sua categoria.

  > O título será obtido automaticamente. Se não for possível, você poderá informá-lo manualmente.

* **Editar Link**: Modifica título e URL de um link existente.

* **Remover Link**: Exclui o link selecionado.

* **Exportar Links** / **Importar Links**: Igual às opções da categoria.

* **Ordenar Links**: Organiza os links em ordem alfabética.

### ⌨️ Atalhos

Os seguintes atalhos estão disponíveis:

| Função              | Atalho                     |
| ------------------- | -------------------------- |
| Abrir Link          | `Alt+B`                    |
| Adicionar Link      | `Alt+A`                    |
| Editar Link         | `Alt+E` ou `F2`            |
| Excluir Link        | `Alt+L` ou `Del`           |
| Adicionar Categoria | `Alt+D`                    |
| Sair                | `Alt+S`, `Esc` ou `Alt+F4` |

## ➕ Diálogo "Adicionar Novo Link"

1. **Categoria**: Selecione a categoria desejada.
2. **URL**: Cole ou digite o endereço do link.

   > Se você já tiver copiado uma URL, ela será colada automaticamente.
3. **OK (`Alt+O`)**: Adiciona o link.

   > O título será buscado automaticamente. Caso não seja possível, você poderá inseri-lo manualmente.
4. **Cancelar (`Alt+C`)**: Fecha o diálogo (`Esc` ou `Alt+F4` também funcionam).

## 📝 Diálogo "Editar Link"

1. **Categoria**: Ao alterar, o link será movido para a nova categoria.
2. **Título**: Edite o título do link.
3. **URL**: Altere o endereço do link.
4. **OK (`Alt+O`)**: Salva as alterações.
5. **Cancelar (`Alt+C`)**: Fecha sem salvar (`Esc` ou `Alt+F4` também funcionam).

## 🙏 Agradecimentos

Um agradecimento especial à **Rue Fontes** e ao **Ângelo Abrantes** pelos testes realizados e pelas sugestões valiosas que contribuíram significativamente para a melhoria deste projeto.

Agradeço também ao **Marlon Brandão de Sousa**, por compartilhar generosamente seu workflow, o que foi crucial para garantir a eficiência e qualidade do desenvolvimento.

## 🌍 Tradutores

* 🇸🇦 **Árabe** — Ahmed Bakr
* 🇧🇷 **Português (Brasil)** — Edilberto Fonseca
* 🇵🇹 **Português (Portugal)** — Edilberto Fonseca
* 🇷🇺 **Russo (Rússia)** — Valentin Kupriyanov
* 🇹🇷 **Turco (Turquia)** — Umut KORKMAZ
* 🇺🇦 **Ucraniano (Ucrânia)** — Heorhii Halas
