# Aplicação Ox

Workspace Cargo virtual da fundação desktop do Ox, versão interna 0.1.0.
Contém 16 crates, o shell Iced e fatias locais de supervisão, plugins e verificação.
Este guia parte da raiz do repositório; para conhecer o produto, veja o
[README principal](../README.md).

[Preparar](#preparar-e-executar) · [Demonstração](#usar-a-demonstração) ·
[Problemas](#resolver-problemas-de-primeiro-uso) · [Testes](#testes-e-referência-rust)

## A demonstração em duas observações

[![Resultado correto aprovado na interface real do Ox](../docs/assets/ox-approved.png)](../docs/assets/ox-approved.png)

*Captura real do corpus Wayland F0 de 03/11/2026. A aprovação vem depois da ação
Verify result; terminar o processo não basta. A imagem conserva os bytes originais.*

## Preparar e executar

Ambiente adotado: Linux x86_64, Rust/Cargo 1.99.1 e sessão X11 ou Wayland.
[Cargo.toml](Cargo.toml) define edition 2024, piso declarado Rust 1.99 e Iced
=0.14.0. Esse piso não é uma demonstração do mínimo técnico suportado.
[rust-toolchain.toml](rust-toolchain.toml) fixa o compilador, rustfmt e clippy;
[Cargo.lock](Cargo.lock) registra as dependências.

Tenha as dependências disponíveis em cache ou acesso autorizado para obtê-las,
além das bibliotecas de sistema exigidas por Iced/winit. A lista de pacotes não
foi validada para todas as distribuições Linux.

```bash
cd application
cargo build --workspace --locked
cargo run --locked -p ox-app --bin ox
```

Para um cache já preparado, acrescente `--offline` a build, run e testes.
`--locked` impede atualizar o lockfile, mas não impede downloads. Um erro de
cache em modo offline exige disponibilizar as dependências antes de repetir.

O build do workspace gera os três binários usados pela demonstração:

| Binário em `target/debug/` | Papel |
| --- | --- |
| `ox` | Interface desktop |
| `local-task` | Produtor controlado do artefato |
| `task-oracle` | Verificador independente do resultado |

A UI procura os auxiliares ao lado do próprio executável. Compilar somente
`ox-app` não prepara necessariamente os outros dois. Ao usar outro perfil ou
diretório de build, mantenha os três juntos.

## Usar a demonstração

Escolha um diretório local de demonstração existente, acessível e gravável.
A validação confere diretório e leitura; a escrita é exercida pela execução.

| Ação na janela | Observação esperada |
| --- | --- |
| **Validate workspace** | Habilita execução se o diretório puder ser validado |
| **Run correct** | Produz `result=42`; permanece `UNVERIFIED` antes de verificar |
| **Verify result** após o cenário correto | Pode aprovar se identidade, oráculo e inputs permanecerem válidos |
| **Run incorrect**, depois **Verify result** | Rejeita `result=41`, apesar da saída bem-sucedida do produtor |
| **Fail** | Exercita término com falha |
| **Timeout** | Exercita o prazo do processo controlado |
| **Cancel** durante uma operação | Solicita cancelamento do processo em andamento |
| **Refresh inputs** | Reavalia a atualidade da evidência pelos bytes dos inputs |

Cada tentativa usa um diretório exclusivo `.ox-task-<sessão>-<tentativa>/`, contendo
`request.txt` e, quando produzido, `result.txt`. Não há monitoramento automático:
após editar um artefato, use **Refresh inputs**. Uma aprovação anterior não vale
para inputs alterados. Falha ou interrupção podem deixar somente o pedido.

**Sair** e fechar a janela solicitam cancelamento e aguardam a operação encerrar.
Os arquivos de tentativa permanecem no workspace. Reiniciar perde o histórico em
memória e não recupera as aprovações a partir desses arquivos.
A [reprodução detalhada](../docs/validation/product-local-task-ui/reproduce.md)
e a [referência de contratos](../docs/architecture/contracts.md) descrevem os casos.


[![Fluxo de primeiro uso com caminhos de sucesso, recusa e evidência insuficiente](../docs/assets/first-run.svg)](../docs/assets/first-run.svg)

*O ciclo inclui recusa do workspace e reavaliação dos inputs, além do caminho correto.* [Abrir em tamanho integral](../docs/assets/first-run.svg).

<details>
<summary>Diagrama Mermaid — fonte editável</summary>

```mermaid
flowchart TD
    accTitle: Da seleção do workspace ao resultado verificado
    accDescr: Validar o diretório habilita a tarefa. Executar produz um candidato ainda não verificado. Verificar exige observação estável do oráculo. Resultado incorreto é rejeitado; interrupção ou instabilidade não aprova. Após editar inputs, atualizar a observação de atualidade.
    W["1 · Validar workspace"] --> D{"Diretório acessível?"}
    D -->|não| FIX["Corrigir caminho ou acesso"]
    FIX --> W
    D -->|sim| RUN["2 · Executar tarefa local"]
    RUN --> RAW["Artefato candidato · UNVERIFIED"]
    RAW --> CHECK["3 · Verify result"]
    CHECK --> RESULT{"Observação aplicável?"}
    RESULT -->|estável e aceita| OK["APPROVED"]
    RESULT -->|estável e contradiz| BAD["REJECTED"]
    RESULT -->|interrompida ou instável| INC["INCONCLUSIVE"]
    RESULT -->|ausente ou ilegível| NONE["UNVERIFIED"]
    OK --> EDIT["Editou um input?"]
    EDIT --> REFRESH["Refresh inputs · reavaliar atualidade"]
    classDef good fill:#ecfdf5,stroke:#047857,color:#064e3b
    classDef bad fill:#fff1f2,stroke:#be123c,color:#881337
    classDef uncertain fill:#fff7ed,stroke:#9a3412,color:#7c2d12
    class OK good
    class BAD bad
    class INC,NONE uncertain
```

</details>

### Resultado incorreto também é um cenário esperado

[![Interface real do Ox exibindo REJECTED após verificar um resultado incorreto](../docs/assets/ox-rejected.png)](../docs/assets/ox-rejected.png)

*Outra captura do mesmo corpus: o oráculo contradiz o artefato produzido. Uma
rejeição observada é diferente de não ter observação. Consulte a
[proveniência das capturas](../docs/assets/README.md#capturas-reais).*

## Resolver problemas de primeiro uso

| Sintoma | Conferir / próximo passo |
| --- | --- |
| Workspace recusado | Caminho existente, diretório e permissão de leitura; a edição do campo invalida a seleção anterior |
| Erro ao criar pedido ou resultado | Permissão de escrita e mensagem retornada pela operação; os arquivos usam criação exclusiva |
| Auxiliar ausente | Executar o build do workspace e conferir os três binários no mesmo diretório |
| Falha ao abrir a janela | Sessão gráfica e variáveis de display; examinar o erro do processo |
| Verificação recusada ou desatualizada | Identidade da tentativa, bytes dos artefatos e estado do oráculo; não deduzir aceitação do exit code do produtor |

Não há execução de prompts ou comandos arbitrários, provedor remoto, sandbox,
captura de stdout/stderr pelo runtime ou persistência durável. O host de plugins
é uma API independente da UI. Esses limites importam ao interpretar resultados
da demonstração e dos testes.

## Testes e referência Rust

Execute em `application/`, depois do build dos auxiliares:

```bash
cargo check --workspace --locked
cargo fmt --all -- --check
cargo test --workspace --locked
cargo test --workspace --locked -- --list
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo doc --workspace --no-deps --locked
```

A referência Rust é gerada em `target/doc/`. Testes de processos e sockets Unix
precisam das permissões correspondentes. A suíte comum não executa os seis testes
desktop marcados como ignorados. Somente em sessão X11 dedicada:

```bash
cargo test --locked -p ox-app --test desktop -- --ignored --nocapture --test-threads=1
```

Esse comando move o ponteiro e interage com janelas. A aceitação Wayland tem
[observações próprias](../docs/validation/f0-resumption-20261103/report.md);
sucesso da suíte comum não substitui essa verificação gráfica.

## Navegar no código

Cada crate mantém fontes em `crates/<nome>/src/` e testes externos, quando
presentes, em `crates/<nome>/tests/`. Não há crate na raiz do workspace.

- [Arquitetura e 16 responsabilidades](../docs/architecture/application.md).
- [Contratos e links para implementação/testes](../docs/architecture/contracts.md).
- [Marcos e direção](../docs/architecture/context.md).
- [Política de atualização de versões](../docs/decisions/version-update-policy.md).
- [Features do produto](../sdd/features/README.md#ox-product).

Atualize este guia quando mudarem build, auxiliares, ações da UI, testes ou
ambiente suportado. Responsabilidade: contribuinte da mudança e mantenedor.
A [revisão visual](../docs/validation/documentation-visuals-20261104/report.md)
distingue os comandos executados dos apenas conferidos no código.

## Encerramento de alterações

Quando a tarefa autorizar verificações, a entrada vigente na raiz é
`./scripts/automate.sh run --surface application`: verificações Rust, cobertura
e ferramentas Cargo, além da governança obrigatória, com dependências offline e
lockfile preservado. `run --scope complete` inclui todas as superfícies e os
complementares; sua seleção depende dos critérios da tarefa. Veja os [limites e diagnóstico](../scripts/README.md). Aceitação gráfica
permanece separada. A limpeza de 09/11/2026 usou somente inspeção e não executou
esses comandos.

## Visual workbench

The native shell provides 27 current/planned destinations, Ctrl+K command search,
three session themes and two densities. See [DESIGN.md](../DESIGN.md) and the
[surface contracts](../docs/design/surfaces.md). Planned screens identify unavailable
backends. `python3 application/tools/build_design.py --check` from the repository
root checks generated roles. `python3 application/tools/native_review.py` runs an
isolated graphical observation when Mutter/PipeWire prerequisites are available.

### Current native composition

Editor e arquivos and Modo de foco provide three build-embedded documents with
selectable file navigation/tabs, line numbers, an origin inspector and contextual
tools. They are read-only demonstrations, not files opened from the selected
workspace. Architecture shows declared Cargo dependencies; agent screens separate
roles from unavailable instances. Preferences remain session-only.

From the repository root, `python3 application/tools/native_composition_review.py
--output <new-directory-name>` exercises the composition in isolated Mutter/Wayland;
use a fresh output name to preserve earlier observations. Prerequisites are Mutter,
PyGObject, GStreamer/PipeWire, Pillow and built Ox/helper binaries.
This graphical command requires the effective environment permissions.

Current results and pending scope are in the
[reference integration report](../docs/validation/visual-integration-20261111/report.md).
Its two native runs and 12 Rust tests do not establish X11 or assistive-technology
acceptance. Source coverage and component contracts remain linked from DESIGN.md.

## Tela inicial: abrir uma pasta e retomar a sessão

A **Central de projetos** começa com **Abrir pasta existente**. Use **Escolher pasta…**
para selecionar um diretório no diálogo gráfico, ou informe o caminho e use
**Validar e abrir pasta** (ou Enter no campo). Confirmar o diálogo valida a pasta
automaticamente. Um diretório válido abre a
tarefa local controlada; nenhuma tarefa é executada durante essa seleção. Quando
o caminho é recusado, a tela mostra o motivo e permite corrigir e validar novamente.

Ao voltar ao início, **Nesta sessão** mostra a pasta validada e **Retomar tarefa
local**. Editar o caminho invalida essa seleção. A lista de projetos não é salva
ao fechar. **Ver atividade e evidências** e **Ajustar aparência** dão acesso aos
recursos existentes. Em janelas estreitas o contexto fica abaixo do formulário.

A [observação da tela inicial](../docs/validation/start-screen-20261114/report.md)
registra testes, capturas e limites desta entrega; ela não renova o aceite histórico
da aplicação inteira.

O seletor gráfico usa o programa GTK `zenity`, instalado separadamente e disponível
no PATH (observado localmente: 4.2.2). O Ox não o instala automaticamente. Se não
estiver disponível ou falhar, uma mensagem orienta a digitação manual. Cancelar
o diálogo preserva o caminho e o trabalho anterior. Apenas um diálogo é aberto
por vez; mudar de contexto ou encerrar o Ox solicita seu encerramento supervisionado.
Nomes que não possam ser representados em UTF-8 são recusados explicitamente,
sem conversão silenciosa. A seleção não cria projetos nem executa tarefas.
