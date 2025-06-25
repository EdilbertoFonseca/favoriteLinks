# Ligações Favoritas

* **Autor**: Edilberto Fonseca ([edilberto.fonseca@outlook.com](mailto:edilberto.fonseca@outlook.com))
* **Data de Criação**: 11/04/2024
* **Licença**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## 📌 Introdução

O extra **FavoriteLinks** é uma ferramenta que permite gerir ligações favoritas de forma organizada e eficiente. Com ele, pode guardar, editar e remover ligações numa lista categorizada. A sua interface intuitiva oferece funcionalidades completas como adicionar novas ligações, editar títulos, remover entradas indesejadas e gerir categorias.

Ao abrir o extra, tem acesso rápido às suas ligações favoritas e pode abrir qualquer ligação seleccionada diretamente no navegador predefinido.

> **Nota**: O extra FavoriteLinks foi desenvolvido com o auxílio do ChatGPT, utilizado tanto para a criação de algumas funções como para a organização e optimização do código.

## 💾 Instalação

Siga os passos abaixo para instalar o extra **FavoriteLinks** no NVDA:

1. **Descarregue o ficheiro de instalação**: Pode obtê-lo a partir da Loja de Extras do NVDA.

   > **Nota**: Se descarregado da loja, a instalação será automática. Caso contrário, siga os passos seguintes.

2. **Instale o extra**: Prima `Enter` sobre o ficheiro `.nvda-addon` descarregado.

3. **Siga as instruções no ecrã**: Conclua a instalação conforme as indicações.

4. **Reinicie o NVDA**: É necessário reiniciar para ativar o extra.

5. **Verifique a instalação**: Pressione `NVDA+N`, vá a *Ferramentas* e confirme se **Ligações Favoritas** está listado.

## ⚙️ Configuração

Pode escolher um local personalizado para guardar o ficheiro de ligações:

1. Aceda ao menu do NVDA: `NVDA+N` > *Preferências* > *Definições*.
2. Na lista de categorias, selecione **Ligações Favoritas**.
3. Utilize o botão **"Selecionar ou adicionar um diretório"** para definir a nova pasta de destino.

## 🚀 Utilização

### Aceder ao Extra

* Prima `Alt+Windows+K`, ou
* Vá a `NVDA+N` > *Ferramentas* > *Ligações Favoritas*.

### Interface Principal

A interface principal apresenta dois campos principais:

1. **Categoria**: Caixa de seleção com as categorias existentes.
2. **Lista de Ligações**: Mostra as ligações associadas à categoria seleccionada.

### Ações Disponíveis

Use o **menu de contexto** (tecla de aplicação) enquanto estiver focado numa das listas para aceder a opções adicionais.

#### Categoria

Na caixa de combinação de categorias, estão disponíveis:

* **Adicionar Categoria**: Cria uma nova categoria.
* **Editar Categoria**: Renomeia a categoria selecionada.
* **Remover Categoria**: Elimina a categoria e as suas ligações.
* **Exportar Ligações**: Guarda as ligações e categorias num ficheiro `.json`.
* **Importar Ligações**: Carrega ligações e categorias a partir de um ficheiro `.json`.

#### Lista de Ligações

Na lista de ligações, estão disponíveis:

* **Abrir Ligação**: Abre a ligação no navegador predefinido.

   > Premir `Enter` também abre a ligação seleccionada.

* **Adicionar Ligação**: Permite inserir um novo URL e atribuir uma categoria.

   > O título será obtido automaticamente. Se tal não for possível, poderá inseri-lo manualmente.

* **Editar Ligação**: Edita o título e URL de uma ligação existente.

* **Remover Ligação**: Elimina a ligação selecionada.

* **Exportar/Importar Ligações**: Igual às opções na secção de categoria.

* **Ordenar Ligações**: Ordena as ligações alfabeticamente.

### ⌨️ Atalhos

Os seguintes atalhos estão disponíveis:

| Função               | Atalho                     |
| -------------------- | -------------------------- |
| Abrir Ligação        | `Alt+B`                    |
| Adicionar Ligação    | `Alt+A`                    |
| Editar Ligação       | `Alt+E` ou `F2`            |
| Eliminar Ligação     | `Alt+L` ou `Del`           |
| Adicionar Categoria  | `Alt+D`                    |
| Sair                 | `Alt+S`, `Esc` ou `Alt+F4` |

## ➕ Diálogo "Adicionar Nova Ligação"

1. **Categoria**: Selecione a categoria desejada.
2. **URL**: Cole ou escreva o endereço da ligação.

   > Se já tiver um URL copiado, ele será inserido automaticamente.
3. **OK (`Alt+O`)**: Adiciona a ligação.

   > O título será recuperado automaticamente. Se não for possível, poderá inseri-lo manualmente.
4. **Cancelar (`Alt+C`)**: Fecha o diálogo (`Esc` ou `Alt+F4` também funcionam).

## 📝 Diálogo "Editar Ligação"

1. **Categoria**: Ao alterar, a ligação será movida para a nova categoria.
2. **Título**: Edite o título da ligação.
3. **URL**: Altere o endereço da ligação.
4. **OK (`Alt+O`)**: Guarda as alterações.
5. **Cancelar (`Alt+C`)**: Fecha sem guardar (`Esc` ou `Alt+F4` também funcionam).

## 🙏 Agradecimentos

Um agradecimento especial à **Rue Fontes** e ao **Ângelo Abrantes** pelos testes realizados e pelas sugestões valiosas que contribuíram significativamente para a melhoria deste projecto.

Agradeço também ao **Marlon Brandão de Sousa**, por partilhar generosamente o seu workflow, o que foi crucial para garantir a eficiência e qualidade do desenvolvimento.

## 🌍 Tradutores

* 🇸🇦 **Árabe** — Ahmed Bakr
* 🇧🇷 **Português (Brasil)** — Edilberto Fonseca
* 🇵🇹 **Português (Portugal)** — Edilberto Fonseca
* 🇷🇺 **Russo (Rússia)** — Valentin Kupriyanov
* 🇹🇷 **Turco (Turquia)** — Umut KORKMAZ
* 🇺🇦 **Ucraniano (Ucrânia)** — Heorhii Halas
