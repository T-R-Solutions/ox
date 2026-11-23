# Capturas finais para aceite visual do mantenedor

Binário Ox observado: `39d517bb89494ba73725c4da2e7e7fd8b326f1abd3c38dce21a88a3593e03f86`.
As imagens são capturas nativas reais, em sessões privadas. Projetos são descartáveis.
Referência: VISUAL STUDIO 2026 ENTERPRISE, mantendo a identidade Ox, conforme DESIGN.md.
AC-07 de product-ide-shell requer julgamento visual explícito do mantenedor.
Este índice não declara aceite técnico ou conclusão da remediação.

| Recorte | Captura |
| --- | --- |
| Central de projetos e recentes reais,1600 | [Central](wc-07/restart/actual-mru-restarted.png) |
| Barra de comandos,1024 | [Barra1024](wc-07/width-1024/command-bar.png) |
| Menu Arquivo aberto e foco após Escape,1024 | [Aberto](wc-07/width-1024/file-menu.png) · [Fechado com foco](wc-07/width-1024/menu-escape-focus.png) |
| Barra e largura de leitura,2560 | [Tarefas2560](wc-07/width-2560/command-bar.png) |
| Editor ocupa largura disponível,2560 | [Editor2560](wc-07/width-2560/full-width-embedded-editor.png) |
| Editor demonstrativo e dock Testes,1600 | [Editor](composition/editor-selected-workbench.png) · [Dock](composition/editor-tool-tests.png) |
| Tarefa e evidência atual,1600 | [Critério aprovado](wayland/task-approved-badge.png) |
| Janela640×480, alto contraste/compacta | [Central640](wc-07/narrow/high-contrast-compact-entry.png) |
| Criar/Cancelar acessíveis por teclado,640×480 | [Confirmação640](wc-07/narrow/create-confirmation-keyboard-focus.png) |
| Destinos nativos | [27capturas e eventos](wayland/result.json) — imagens S01–S14,W00,A01–A06,TW01–TW04,SDD,SKL no diretório wayland |

WC07 executou integralmente as sete sessões, sem reduzir seleção; resultado e identidades em [result.json](wc-07/result.json). Cada sessão exige saída natural0, geometria Wayland confirmada, oráculos de arquivos/PIDs e nenhuma mudança dos inputs. Capturas ainda requerem inspeção visual; não equivalem a leitor de tela, portal padrão ou outros compositores.

Tentativas anteriores permanecem preservadas: WC01 falha de canal de observação; WC02 Escape do campo de localização GTK; WC03 ciclo do socket do helper; WC04 rótulo de largura/menu1024 inconclusivo; WC05 espera de frame em cena estática; WC06 continuação delimitada. Nenhuma delas foi rebatizada como execução integral bem-sucedida. A decisão visual atual deve usar WC07 e as entradas Wayland finais deste índice.
