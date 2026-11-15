use super::{
    Appearance, ButtonRole, Density, Desktop, Element, EvidenceState, HistoryAction, Message,
    Surface,
};
use crate::design::{self, CODE_FONT, HEADING_FONT};
use iced::{
    Alignment, Color, Length,
    widget::{column, container, row, rule, scrollable, space, text, text_input},
};

// TextInput owns native focus. Observe it after pointer handling, including
// captured clicks, so Desktop's button traversal cannot retain a stale target.
struct TrackedInput<'a> {
    input: Element<'a, Message>,
    id: usize,
}
struct InputFocusProbe(bool);
impl iced::advanced::widget::Operation for InputFocusProbe {
    fn traverse(&mut self, operate: &mut dyn FnMut(&mut dyn iced::advanced::widget::Operation)) {
        operate(self);
    }
    fn focusable(
        &mut self,
        _: Option<&iced::widget::Id>,
        _: iced::Rectangle,
        state: &mut dyn iced::advanced::widget::operation::Focusable,
    ) {
        self.0 |= state.is_focused();
    }
}
impl iced::advanced::Widget<Message, iced::Theme, iced::Renderer> for TrackedInput<'_> {
    fn size(&self) -> iced::Size<Length> {
        self.input.as_widget().size()
    }
    fn size_hint(&self) -> iced::Size<Length> {
        self.input.as_widget().size_hint()
    }
    fn tag(&self) -> iced::advanced::widget::tree::Tag {
        self.input.as_widget().tag()
    }
    fn state(&self) -> iced::advanced::widget::tree::State {
        self.input.as_widget().state()
    }
    fn children(&self) -> Vec<iced::advanced::widget::Tree> {
        self.input.as_widget().children()
    }
    fn diff(&self, tree: &mut iced::advanced::widget::Tree) {
        self.input.as_widget().diff(tree);
    }
    fn layout(
        &mut self,
        tree: &mut iced::advanced::widget::Tree,
        renderer: &iced::Renderer,
        limits: &iced::advanced::layout::Limits,
    ) -> iced::advanced::layout::Node {
        self.input.as_widget_mut().layout(tree, renderer, limits)
    }
    fn operate(
        &mut self,
        tree: &mut iced::advanced::widget::Tree,
        layout: iced::advanced::Layout<'_>,
        renderer: &iced::Renderer,
        operation: &mut dyn iced::advanced::widget::Operation,
    ) {
        self.input
            .as_widget_mut()
            .operate(tree, layout, renderer, operation);
    }
    fn update(
        &mut self,
        tree: &mut iced::advanced::widget::Tree,
        event: &iced::Event,
        layout: iced::advanced::Layout<'_>,
        cursor: iced::mouse::Cursor,
        renderer: &iced::Renderer,
        clipboard: &mut dyn iced::advanced::Clipboard,
        shell: &mut iced::advanced::Shell<'_, Message>,
        viewport: &iced::Rectangle,
    ) {
        self.input.as_widget_mut().update(
            tree, event, layout, cursor, renderer, clipboard, shell, viewport,
        );
        if matches!(
            event,
            iced::Event::Mouse(iced::mouse::Event::ButtonPressed(iced::mouse::Button::Left))
                | iced::Event::Touch(iced::touch::Event::FingerPressed { .. })
        ) {
            let mut focus = InputFocusProbe(false);
            self.input
                .as_widget_mut()
                .operate(tree, layout, renderer, &mut focus);
            if focus.0 {
                shell.publish(Message::InputFocused(self.id));
            }
        }
    }
    fn draw(
        &self,
        tree: &iced::advanced::widget::Tree,
        renderer: &mut iced::Renderer,
        theme: &iced::Theme,
        style: &iced::advanced::renderer::Style,
        layout: iced::advanced::Layout<'_>,
        cursor: iced::mouse::Cursor,
        viewport: &iced::Rectangle,
    ) {
        self.input
            .as_widget()
            .draw(tree, renderer, theme, style, layout, cursor, viewport);
    }
    fn mouse_interaction(
        &self,
        tree: &iced::advanced::widget::Tree,
        layout: iced::advanced::Layout<'_>,
        cursor: iced::mouse::Cursor,
        viewport: &iced::Rectangle,
        renderer: &iced::Renderer,
    ) -> iced::mouse::Interaction {
        self.input
            .as_widget()
            .mouse_interaction(tree, layout, cursor, viewport, renderer)
    }
    fn overlay<'a>(
        &'a mut self,
        tree: &'a mut iced::advanced::widget::Tree,
        layout: iced::advanced::Layout<'a>,
        renderer: &iced::Renderer,
        viewport: &iced::Rectangle,
        translation: iced::Vector,
    ) -> Option<iced::advanced::overlay::Element<'a, Message, iced::Theme, iced::Renderer>> {
        self.input
            .as_widget_mut()
            .overlay(tree, layout, renderer, viewport, translation)
    }
}
impl<'a> From<TrackedInput<'a>> for Element<'a, Message> {
    fn from(input: TrackedInput<'a>) -> Self {
        Self::new(input)
    }
}

impl Desktop {
    fn tracked_input<'a>(
        input: impl Into<Element<'a, Message>>,
        id: usize,
    ) -> Element<'a, Message> {
        TrackedInput {
            input: input.into(),
            id,
        }
        .into()
    }
    fn paragraph<'a>(&self, value: impl Into<std::borrow::Cow<'a, str>>) -> Element<'a, Message> {
        text(value.into())
            .size(15)
            .color(self.appearance.palette().text_secondary)
            .width(Length::Fill)
            .into()
    }
    fn section<'a>(
        &self,
        title: &'a str,
        caption: &'a str,
        body: Element<'a, Message>,
    ) -> Element<'a, Message> {
        let p = self.appearance.palette();
        let mut content = column![text(title).font(HEADING_FONT).size(16)];
        if !caption.is_empty() {
            content = content.push(text(caption).size(13).color(p.text_muted));
        }
        content = content.push(body).spacing(self.density.gap());
        container(content)
            .padding(self.density.inset())
            .width(Length::Fill)
            .style(move |_| design::panel(p.surface_base, p.text_primary, p.border_decorative))
            .into()
    }
    fn notice<'a>(
        &self,
        title: &'a str,
        description: impl Into<std::borrow::Cow<'a, str>>,
    ) -> Element<'a, Message> {
        let p = self.appearance.palette();
        container(
            column![
                text(title).font(HEADING_FONT).size(14),
                text(description.into()).size(14)
            ]
            .spacing(6),
        )
        .padding(12)
        .width(Length::Fill)
        .style(move |_| design::panel(p.surface_recessed, p.text_secondary, p.border_decorative))
        .into()
    }
    fn unavailable<'a>(&self, action: &'a str) -> Element<'a, Message> {
        column![
            self.notice("Backend não integrado", self.surface.dependency()),
            self.control(900, action, None)
        ]
        .spacing(12)
        .into()
    }
    fn badge(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let state = EvidenceState::from_status(&self.status);
        let (fg, bg) = if self.busy {
            (p.domain_execution_fg, p.domain_execution_bg)
        } else {
            state.colors(p)
        };
        let label = if self.closing {
            "Encerrando · aguarde"
        } else if self.busy {
            "Operação em andamento"
        } else {
            state.label()
        };
        container(
            row![
                text(if state == EvidenceState::Approved && !self.busy {
                    "✓"
                } else {
                    "•"
                })
                .size(14),
                text(label).size(13)
            ]
            .spacing(6),
        )
        .padding([5, 9])
        .style(move |_| design::panel(bg, fg, bg))
        .into()
    }
    fn workspace(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let available = self.project_available();
        let input = text_input("/caminho/do/projeto", &self.path)
            .id("workspace")
            .size(15)
            .padding(10)
            .style(move |_, status| {
                let focused = matches!(status, text_input::Status::Focused { .. });
                text_input::Style {
                    background: p.surface_base.into(),
                    border: iced::Border {
                        color: if focused {
                            p.focus
                        } else {
                            p.border_interactive
                        },
                        width: if focused { 2.0 } else { 1.0 },
                        radius: 4.0.into(),
                    },
                    icon: p.icon_primary,
                    placeholder: p.text_muted,
                    value: p.text_primary,
                    selection: p.surface_selected,
                }
            });
        let input = if available {
            input.on_input(Message::Path).on_submit(Message::Select)
        } else {
            input
        };
        let input = Self::tracked_input(input, 2);
        let entry = self.surface == Surface::Start;
        let path_control: Element<'_, Message> = if entry {
            row![
                input,
                self.control(
                    273,
                    "Escolher pasta…",
                    (available && self.picker.is_none()).then_some(Message::ChooseFolder)
                )
            ]
            .spacing(8)
            .align_y(Alignment::Center)
            .into()
        } else {
            input
        };
        let mut form = column![
            text("Caminho de um diretório existente").size(14),path_control,
            row![self.styled_control(3,if entry {"Validar e abrir pasta"} else {"Validar diretório"},available.then_some(Message::Select),if entry && self.selected {ButtonRole::Secondary} else {ButtonRole::Primary}),text(if self.selected{"Diretório validado"}else if self.busy {"Operação em andamento"} else {"Validação necessária"}).size(13).color(p.text_secondary)].spacing(12).align_y(Alignment::Center).wrap(),
            self.paragraph(if entry {"A pasta será validada antes de abrir a tarefa local. Nenhuma tarefa é executada nesta etapa."} else {"A execução cria uma pasta exclusiva de tentativa. Seus arquivos existentes são preservados."})
        ].spacing(12);
        if entry && self.picker.is_some() {
            form = form.push(
                self.paragraph("Seletor de pasta aberto. Cancelar preserva o trabalho atual."),
            );
        }
        if entry && let Some(error) = &self.picker_error {
            form = form.push(self.notice("Não foi possível escolher a pasta", error.clone()));
        }
        if let Some(error) = &self.workspace_error {
            form = form.push(
                container(
                    column![
                        text("Não foi possível abrir a pasta")
                            .font(HEADING_FONT)
                            .size(15),
                        text(error).size(14).wrapping(text::Wrapping::WordOrGlyph),
                        text("Revise o caminho e valide novamente.").size(14)
                    ]
                    .spacing(6),
                )
                .padding(12)
                .width(Length::Fill)
                .style(move |_| design::panel(p.error_bg, p.error_fg, p.border_decorative)),
            );
        }
        self.section(
            if entry {
                "Abrir pasta existente"
            } else {
                "Diretório do projeto"
            },
            if entry {
                "Trabalhe a partir dos arquivos no seu computador"
            } else {
                "Seleção local · nenhum processo é iniciado ao validar"
            },
            form.into(),
        )
    }
    fn welcome_control<'a>(
        &self,
        id: usize,
        label: &'a str,
        message: Option<Message>,
        role: ButtonRole,
    ) -> Element<'a, Message> {
        container(self.styled_control(id, label, message, role))
            .id(format!("welcome-control-{id}"))
            .into()
    }
    fn welcome_error(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let mut errors = column![].spacing(10);
        if let Some(error) = &self.workspace_error {
            errors = errors.push(container(column![
                text("Não foi possível abrir o projeto").font(HEADING_FONT).size(15),
                text(error).size(14).wrapping(text::Wrapping::WordOrGlyph),
                text(if self.surface == Surface::NewProject {"Revise o nome e a pasta de destino."} else {"Escolha outra pasta ou revise o caminho. Se for um projeto recente, você também pode removê-lo da lista."}).size(14)
            ].spacing(6)).padding(12).width(Length::Fill).style(move |_| design::panel(p.error_bg, p.error_fg, p.border_decorative)));
        }
        if let Some(error) = &self.picker_error {
            errors = errors.push(self.notice("Seletor de pastas indisponível", error.as_str()));
        }
        errors.into()
    }
    fn start_view(&self) -> Element<'_, Message> {
        let intro = self.start_intro_view();
        let recent = self.recent_projects_view();
        if self.width > 1024.0 {
            row![
                container(intro).width(Length::FillPortion(2)),
                container(recent).width(Length::FillPortion(3))
            ]
            .spacing(48)
            .into()
        } else {
            column![intro, rule::horizontal(1), recent]
                .spacing(28)
                .into()
        }
    }
    fn start_intro_view(&self) -> Element<'_, Message> {
        let available = self.project_available();
        let mut intro = column![
            text("Bem-vindo ao Ox").font(HEADING_FONT).size(24),
            self.paragraph("Seu próximo projeto começa aqui."),
            self.paragraph("Abra uma pasta do computador ou crie um projeto vazio."),
            row![
                self.welcome_control(
                    273,
                    "Abrir pasta…",
                    available.then_some(Message::ChooseFolder),
                    ButtonRole::Primary
                ),
                self.welcome_control(
                    274,
                    "Novo projeto",
                    available.then_some(Message::Navigate(Surface::NewProject)),
                    ButtonRole::Secondary
                )
            ]
            .spacing(10)
            .wrap(),
        ]
        .spacing(14);
        if self.selected {
            intro = intro.push(self.welcome_control(
                270,
                "Retomar projeto aberto",
                (!self.closing).then_some(Message::Navigate(Surface::Tasks)),
                ButtonRole::Secondary,
            ));
        }
        intro = intro.push(self.welcome_control(
            275,
            if self.manual_path {
                "Ocultar caminho manual"
            } else {
                "Digitar caminho…"
            },
            available.then_some(Message::ManualPath),
            ButtonRole::Navigation(false),
        ));
        if self.manual_path {
            let input = text_input("/caminho/do/projeto", &self.path)
                .id("workspace")
                .size(15)
                .padding(10);
            let input = if available {
                input.on_input(Message::Path).on_submit(Message::Select)
            } else {
                input
            };
            intro = intro.push(
                column![
                    text("Caminho da pasta").font(HEADING_FONT).size(14),
                    container(Self::tracked_input(input, 2)).id("welcome-control-2"),
                    self.welcome_control(
                        3,
                        "Abrir caminho",
                        available.then_some(Message::Select),
                        ButtonRole::Secondary
                    )
                ]
                .spacing(8),
            );
        }
        if self.picker.is_some() {
            intro = intro.push(self.paragraph(
                "Escolha uma pasta na janela aberta. Cancelar preserva o projeto atual.",
            ));
        }
        if self.busy {
            intro = intro.push(self.paragraph("Abrindo projeto…"));
        }
        intro = intro.push(self.welcome_error());
        intro.into()
    }
    fn recent_projects_view(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let available = self.project_available();
        let mut recent = column![text("Projetos recentes").font(HEADING_FONT).size(20)].spacing(12);
        if self.history_busy {
            recent = recent.push(self.paragraph("Carregando histórico…"));
        } else if self.recent.is_empty() {
            recent = recent.push(self.paragraph("Os projetos que você abrir aparecerão aqui."));
        }
        if let Some(error) = &self.history_error {
            recent = recent
                .push(self.notice("Histórico indisponível", error.as_str()))
                .push(
                    row![
                        self.welcome_control(
                            280,
                            "Tentar novamente",
                            available.then_some(Message::History(HistoryAction::Load)),
                            ButtonRole::Secondary
                        ),
                        self.welcome_control(
                            281,
                            "Redefinir histórico…",
                            available.then_some(Message::ResetConfirmation(true)),
                            ButtonRole::Navigation(false)
                        )
                    ]
                    .spacing(8)
                    .wrap(),
                );
            if self.reset_confirmation {
                recent = recent.push(self.notice("Redefinir a lista de projetos?", "A lista será esvaziada. Se o arquivo estiver corrompido, uma cópia será preservada. Seus projetos não serão alterados. Arquivos grandes demais ou de versões futuras serão preservados e a redefinição será recusada."))
                    .push(row![
                        self.welcome_control(282, "Redefinir recentes", available.then_some(Message::History(HistoryAction::Reset)), ButtonRole::Danger),
                        self.welcome_control(283, "Cancelar", Some(Message::ResetConfirmation(false)), ButtonRole::Secondary)
                    ].spacing(8).wrap());
            }
        }
        for (i, path) in self.recent.iter().enumerate() {
            let id = 400 + i * 2;
            let name = path
                .file_name()
                .and_then(|n| n.to_str())
                .unwrap_or("Projeto local");
            let focused = self.focus == Some(id);
            let open = iced::widget::button(
                column![
                    text(name)
                        .font(HEADING_FONT)
                        .size(16)
                        .wrapping(text::Wrapping::WordOrGlyph),
                    text(path.to_str().expect("history is UTF-8"))
                        .size(14)
                        .color(p.text_secondary)
                        .wrapping(text::Wrapping::WordOrGlyph)
                ]
                .spacing(5)
                .width(Length::Fill),
            )
            .on_press_maybe(available.then_some(Message::OpenRecent(path.clone())))
            .padding(12)
            .width(Length::Fill)
            .style(move |_, status| {
                design::button_style(p, ButtonRole::Navigation(false), focused, status)
            });
            recent = recent.push(
                container(
                    row![
                        container(open)
                            .id(format!("welcome-control-{id}"))
                            .width(Length::Fill),
                        self.welcome_control(
                            id + 1,
                            "Remover",
                            available
                                .then_some(Message::History(HistoryAction::Remove(path.clone()))),
                            ButtonRole::Navigation(false)
                        )
                    ]
                    .spacing(6)
                    .align_y(Alignment::Center),
                )
                .width(Length::Fill)
                .style(move |_| design::panel(p.surface_base, p.text_primary, p.border_decorative)),
            );
        }
        recent.into()
    }
    fn new_project_view(&self) -> Element<'_, Message> {
        let available = self.project_available();
        let name = text_input("meu-projeto", &self.project_name)
            .id("project-name")
            .size(16)
            .padding(10);
        let name = if available {
            name.on_input(Message::ProjectName)
                .on_submit(Message::InputFocused(290))
        } else {
            name
        };
        let parent = text_input("/caminho/da/pasta", &self.project_parent)
            .id("project-parent")
            .size(15)
            .padding(10);
        let parent = if available {
            parent
                .on_input(Message::ProjectParent)
                .on_submit(Message::InputFocused(291))
        } else {
            parent
        };
        let destination = std::path::Path::new(&self.project_parent).join(&self.project_name);
        let mut body = column![
            text("Novo projeto").font(HEADING_FONT).size(22),
            self.paragraph("Crie uma pasta vazia para começar."),
            text("Nome do projeto").font(HEADING_FONT).size(14),
            container(Self::tracked_input(name, 290)).id("welcome-control-290"),
            text("Criar dentro de · caminho absoluto").font(HEADING_FONT).size(14),
            container(Self::tracked_input(parent, 291)).id("welcome-control-291"),
            self.welcome_control(292, "Escolher pasta de destino…", available.then_some(Message::ChooseFolder), ButtonRole::Secondary),
            self.notice("Destino completo", if !std::path::Path::new(&self.project_parent).is_absolute() || self.project_name.is_empty() {"Preencha o nome e o caminho absoluto da pasta de destino.".into()} else {destination.display().to_string()}),
            self.paragraph("Criar e abrir cria somente uma pasta vazia no destino acima. Arquivos existentes são preservados; nenhuma tarefa ou comando é iniciado."),
            self.welcome_error(),
        ].spacing(12);
        if self.busy {
            body = body.push(self.paragraph(
                "Criando e abrindo o projeto… Aguarde o resultado antes de tentar novamente.",
            ));
        }
        if self.picker.is_some() {
            body = body.push(self.paragraph("Selecione a pasta que receberá o novo projeto."));
        }
        body = body.push(
            row![
                self.welcome_control(
                    293,
                    "Criar e abrir",
                    available.then_some(Message::CreateProject),
                    ButtonRole::Primary
                ),
                self.welcome_control(
                    294,
                    "Cancelar",
                    (!self.busy && !self.closing).then_some(Message::Navigate(Surface::Start)),
                    ButtonRole::Secondary
                )
            ]
            .spacing(10)
            .wrap(),
        );
        container(body).max_width(660).into()
    }
    fn welcome_view(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let header = container(
            row![
                text("Ox").font(HEADING_FONT).size(23),
                space::horizontal(),
                self.control(
                    272,
                    "Configurações",
                    Some(Message::Navigate(Surface::Settings))
                )
            ]
            .align_y(Alignment::Center)
            .spacing(12),
        )
        .padding([16, 24])
        .width(Length::Fill);
        let content = if self.surface == Surface::NewProject {
            self.new_project_view()
        } else {
            self.start_view()
        };
        let body = scrollable(
            container(container(content).max_width(1000).width(Length::Fill))
                .padding(if self.width < 700.0 { 20 } else { 36 })
                .center_x(Length::Fill),
        )
        .id("main")
        .width(Length::Fill)
        .height(Length::Fill);
        container(column![header, body].height(Length::Fill))
            .height(Length::Fill)
            .width(Length::Fill)
            .style(move |_| container::Style {
                background: Some(p.workbench_bg.into()),
                text_color: Some(p.text_primary),
                ..Default::default()
            })
            .into()
    }
    fn task_actions(&self) -> Element<'_, Message> {
        let available = !self.busy && !self.closing;
        let start = available && self.selected;
        let verify = available && self.result;
        self.section("Tarefa local controlada","Escolha um cenário. O término do processo não aprova o resultado.",column![
            row![
                self.styled_control(4,"Executar correto",start.then_some(Message::Start("good")),ButtonRole::Primary),
                self.control(5,"Executar incorreto",start.then_some(Message::Start("bad"))),
                self.control(6,"Provocar falha",start.then_some(Message::Start("failure"))),
                self.control(7,"Exercitar prazo",start.then_some(Message::Start("hang")))
            ].spacing(8).wrap(),
            rule::horizontal(1),
            row![
                self.styled_control(8,"Cancelar operação",self.busy.then_some(Message::Cancel),ButtonRole::Danger),
                self.styled_control(9,"Verificar resultado",verify.then_some(Message::Verify),ButtonRole::Primary),
                self.control(10,"Atualizar inputs",verify.then_some(Message::Refresh))
            ].spacing(8).wrap(),
            self.paragraph("Prazo do subprocesso: 10 segundos. Cancelamento e fechamento aguardam o término observado; não prometem desfazer arquivos.")
        ].spacing(12).into())
    }
    fn evidence(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let raw = column(self.status.lines().map(|line| {
            text(line)
                .size(13)
                .font(CODE_FONT)
                .wrapping(text::Wrapping::WordOrGlyph)
                .width(Length::Fill)
                .into()
        }))
        .spacing(0);
        self.section("Observação e evidências","Diagnóstico original · histórico em memória · atualidade depende de atualização explícita",column![
            self.badge(),
            self.paragraph("Aprovação técnica vale para o critério e os inputs observados. Aceite humano não é registrado por este fluxo."),
            container(raw).padding(12).width(Length::Fill).style(move |_|design::panel(p.unknown_bg,p.text_primary,p.border_decorative))
        ].spacing(12).into())
    }
    fn appearance_view(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let themes = row(Appearance::ALL.iter().enumerate().map(|(i, a)| {
            self.styled_control(
                220 + i,
                a.label(),
                Some(Message::Appearance(*a)),
                ButtonRole::Navigation(self.appearance == *a),
            )
            .into()
        }))
        .spacing(8)
        .wrap();
        let density = row![
            self.styled_control(
                223,
                "Confortável",
                Some(Message::Density(Density::Comfortable)),
                ButtonRole::Navigation(self.density == Density::Comfortable)
            ),
            self.styled_control(
                224,
                "Compacta",
                Some(Message::Density(Density::Compact)),
                ButtonRole::Navigation(self.density == Density::Compact)
            )
        ]
        .spacing(8)
        .wrap();
        let swatches = row![
            Self::color_sample("Identidade", p.shell_bg, p.text_shell),
            Self::color_sample("Ação", p.action_bg, p.action_text),
            Self::color_sample("Verificação", p.success_bg, p.success_fg),
            Self::color_sample("Atenção", p.warning_bg, p.warning_fg),
            Self::color_sample("Falha", p.error_bg, p.error_fg),
            Self::color_sample("Inferência", p.inferred_bg, p.inferred_fg)
        ]
        .spacing(8)
        .wrap();
        column![
            self.notice("Preferências desta sessão","Mudanças são imediatas e reversíveis. Reiniciar restaura Claro / Confortável; não há persistência de preferências."),
            self.section("Tema da bancada","Escuro e alto contraste são candidatos nativos em avaliação.",column![themes,swatches].spacing(16).into()),
            self.section("Densidade","Espaçamento e altura dos controles mudam; texto e código mantêm o tamanho.",density.into()),
            self.section("Tipografia","IBM Plex Sans + IBM Plex Mono · arquivos nativos incorporados sob SIL OFL 1.1",column![
                text("Intenção → execução → evidência → decisão").size(20).font(HEADING_FONT),
                text("ação · verificação · permissões · 0/O · 1/l/I").size(15),
                text("fn verify(result: &Artifact) -> Verdict { /* origem + inputs */ }").font(CODE_FONT).size(15).wrapping(text::Wrapping::WordOrGlyph),
                self.paragraph("Inter / JetBrains Mono e as categorias cromáticas R13 permanecem propostas; não foram ativadas silenciosamente.")
            ].spacing(12).into()),
            self.section("Prévia de estados","Cor acompanha texto e forma; a prévia abaixo não é um resultado de teste.",self.notice("DEMONSTRAÇÃO DE COMPONENTE","Implementada ≠ Verificada ≠ Aceita. Desconhecida ≠ Inferida. Tema do editor será uma preferência independente quando o editor estiver integrado."))
        ].spacing(self.density.gap()).into()
    }
    fn color_sample(label: &str, bg: Color, fg: Color) -> Element<'_, Message> {
        container(text(label).size(13))
            .padding([12, 16])
            .style(move |_| design::panel(bg, fg, bg))
            .into()
    }
    #[expect(
        clippy::too_many_lines,
        reason = "Embedded document composition keeps one view and its local widget lifetimes together (view composition)"
    )]
    fn document_view(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let names = ["shell.rs", "workbench.rs", "Cargo.toml"];
        let sources = [
            include_str!("../shell.rs"),
            include_str!("../workbench.rs"),
            include_str!("../../Cargo.toml"),
        ];
        let mut files = column![
            text("ARQUIVOS DE REFERÊNCIA").size(12),
            text("ox-ui / fonte embutida").size(13)
        ]
        .spacing(8);
        let mut tabs = row![].spacing(4);
        for (index, name) in names.iter().enumerate() {
            files = files.push(
                self.styled_control(
                    250 + index,
                    name,
                    Some(Message::DemoDocument(index)),
                    ButtonRole::Navigation(index == self.demo_document),
                )
                .width(Length::Fill),
            );
            // Tabs and tree share selection, but retain distinct focus targets.
            tabs = tabs.push(self.styled_control(
                253 + index,
                name,
                Some(Message::DemoDocument(index)),
                ButtonRole::Navigation(index == self.demo_document),
            ));
        }
        let source = sources[self.demo_document];
        let code = column(source.lines().enumerate().map(|(i, line)| {
            row![
                text(format!("{:>3}", i + 1))
                    .font(CODE_FONT)
                    .size(13)
                    .color(p.text_muted)
                    .width(40),
                text(line)
                    .font(CODE_FONT)
                    .size(15)
                    .wrapping(text::Wrapping::WordOrGlyph)
                    .width(Length::Fill)
            ]
            .spacing(12)
            .into()
        }))
        .spacing(5);
        let editor = container(
            column![
                tabs.wrap(),
                text(format!(
                    "ox-ui / {} · somente leitura",
                    names[self.demo_document]
                ))
                .size(13),
                scrollable(code).height(360)
            ]
            .spacing(10),
        )
        .padding(12)
        .width(Length::Fill)
        .style(move |_| design::panel(p.editor_bg, p.text_primary, p.border_interactive));
        let inspector = self.section("Inspeção", "Origem e limites", column![
            self.paragraph(format!("Arquivo: {}", names[self.demo_document])),
            self.paragraph(format!("{} linhas · UTF-8", source.lines().count())),
            self.paragraph("Origem: fonte do Ox incorporada no build. Não corresponde ao diretório selecionado."),
            self.paragraph("Leitura demonstrativa. Salvar, LSP e alterações concorrentes aguardam serviço de documentos.")
        ].spacing(10).into());
        let work: Element<'_, Message> = if self.width >= 1400.0 && self.surface != Surface::Focus {
            row![
                container(files).width(180),
                editor,
                container(inspector).width(240)
            ]
            .spacing(12)
            .into()
        } else {
            column![files, editor, inspector].spacing(12).into()
        };
        let mut tools = row![].spacing(8);
        for (i, label) in ["Problemas", "Testes", "Rastro"].iter().enumerate() {
            tools = tools.push(self.styled_control(
                260 + i,
                label,
                Some(Message::DemoTool(i)),
                ButtonRole::Navigation(self.demo_tool == i),
            ));
        }
        let tool = match self.demo_tool {
            0 => self.notice(
                "Sem provedor de diagnósticos",
                "Não integrado · ausência de dados não significa ausência de problemas.",
            ),
            1 => self.notice(
                "Testes do documento indisponíveis",
                "A verificação da tarefa controlada é independente e permanece na tela Testes.",
            ),
            _ => self.notice(
                "Rastro do documento indisponível",
                "Nenhum evento de edição ou processo foi produzido por esta demonstração.",
            ),
        };
        column![self.notice("DEMONSTRAÇÃO · arquivos embutidos", "Selecione um arquivo na árvore ou nas abas. Nenhuma leitura ou escrita no seu projeto é realizada."),work,
            self.section("Ferramentas", "Contexto do documento", column![tools.wrap(),tool].spacing(10).into())].spacing(self.density.gap()).into()
    }
    fn relationship_map(&self) -> Element<'_, Message> {
        let node = |title, caption| self.notice(title, caption);
        let map: Element<'_, Message> = if self.width >= 1200.0 {
            row![
                container(node("ox-app", "Entrada da aplicação")).width(160),
                text("→").size(24),
                container(node("ox-ui", "Apresentação")).width(160),
                text("→").size(24),
                column![
                    node("ox-agent", "Supervisão"),
                    node("ox-verification", "Critérios e snapshots")
                ]
                .spacing(12)
            ]
            .spacing(12)
            .align_y(Alignment::Center)
            .into()
        } else {
            column![
                node("ox-app", "↓ depende de ox-ui"),
                node("ox-ui", "↓ depende de ox-agent e ox-verification"),
                node("ox-agent / ox-verification", "Supervisão / evidência")
            ]
            .spacing(8)
            .into()
        };
        column![map,self.paragraph("Origem: manifests Cargo do Ox. Setas representam dependências declaradas, não chamadas extraídas ou atividade em execução.")].spacing(12).into()
    }
    fn agent_roles(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let mut rows = column![
            row![
                text("PAPEL").width(Length::Fill),
                text("RESPONSABILIDADE").width(Length::Fill),
                text("INSTÂNCIA").width(Length::Fill)
            ]
            .spacing(12)
        ]
        .spacing(10);
        for (role, purpose) in [
            ("Planejador", "Intenção e etapas"),
            ("Implementador", "Alterações propostas"),
            ("Revisor", "Inspeção independente"),
            ("Verificador", "Critérios e evidências"),
        ] {
            rows = rows.push(rule::horizontal(1)).push(
                row![
                    text(role).size(14).width(Length::Fill),
                    text(purpose).size(14).width(Length::Fill),
                    text("Não integrada")
                        .size(14)
                        .color(p.text_muted)
                        .width(Length::Fill)
                ]
                .spacing(12),
            );
        }
        self.section(
            "Papéis de referência",
            "DEMONSTRAÇÃO · não configura agentes nem inicia instâncias",
            rows.into(),
        )
    }
    fn architecture_view(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let mode = row![
            self.styled_control(
                240,
                "Estrutural",
                Some(Message::GraphMode(false)),
                ButtonRole::Navigation(!self.graph_exploratory)
            ),
            self.styled_control(
                241,
                "Exploratório",
                Some(Message::GraphMode(true)),
                ButtonRole::Navigation(self.graph_exploratory)
            )
        ]
        .spacing(8)
        .wrap();
        let title = if self.graph_exploratory {
            "Modo exploratório · consulta do grafo pendente"
        } else {
            "Modo estrutural · mapa documental da fundação"
        };
        self.section(title,"Relações declaradas no código do Ox; não extraídas do diretório selecionado",column![
            mode,
            self.relationship_map(),
            container(text("Confirmada: linha contínua + origem. Inferida: tracejado + hipótese. Desconhecida: ausência de confirmação.").size(14)).padding(12).style(move |_|design::panel(p.domain_architecture_bg,p.domain_architecture_fg,p.border_decorative)),
            self.unavailable("Consultar grafo do projeto · não integrado")
        ].spacing(12).into())
    }
    fn observability_view(&self) -> Element<'_, Message> {
        let metric = |label| {
            self.section(
                label,
                "Fonte ainda não integrada",
                column![
                    text("—").font(HEADING_FONT).size(28),
                    self.paragraph("Indisponível · não significa zero")
                ]
                .spacing(6)
                .into(),
            )
        };
        column![
            row![metric("Tokens consumidos"),metric("Cache utilizado")].spacing(12).wrap(),
            row![metric("Custo observado"),metric("Contexto atual")].spacing(12).wrap(),
            self.section("Séries e proveniência","Sem coletor, período ou amostras",self.notice("Sem dados disponíveis","Não há série temporal a desenhar. Quando houver dados, cada série terá unidade, período, escopo e origem; estimativas serão identificadas.")),
            self.unavailable("Inspecionar métricas · não integrado")
        ].spacing(self.density.gap()).into()
    }
    fn review_view(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        column![
            self.section("Alterações e verificação","Exemplo de composição · nenhum arquivo foi alterado por esta tela",column![
                self.notice("DEMONSTRAÇÃO DE DIFF","Dados sintéticos para avaliar legibilidade de adições e remoções; não representam mudanças do seu projeto."),
                container(text("− result=41").font(CODE_FONT).size(15)).padding(10).width(Length::Fill).style(move |_|design::panel(p.diff_remove_bg,p.error_fg,p.error_fg)),
                container(text("+ result=42").font(CODE_FONT).size(15)).padding(10).width(Length::Fill).style(move |_|design::panel(p.diff_add_bg,p.success_fg,p.success_fg)),
                self.unavailable("Aceitar alterações · não integrado")
            ].spacing(12).into()),self.evidence()
        ].spacing(self.density.gap()).into()
    }
    fn capability_view(&self) -> Element<'_, Message> {
        let body:Element<'_,Message>=match self.surface {
            Surface::Agents|Surface::AgentSettings|Surface::Orchestration=>column![
                self.agent_roles(),
                self.section("Definições e instâncias","Papéis não são estados de execução",column![
                    self.notice("Nenhum agente de IA conectado","O runtime local supervisiona processos controlados. Isso não configura um provedor ou uma instância de agente."),
                    self.paragraph("Contrato da instância: definição → tarefa → execução/tentativa → atividade → evidência. Permissões e confirmação pertencem ao domínio."),
                    self.unavailable("Configurar instância · não integrado")
                ].spacing(12).into()),
                self.section("Plano e dependências","Composição da futura supervisão",self.notice("Sem plano de orquestração","Etapas terão identidade e dependências. Etapas concluídas não serão convertidas em porcentagem de tempo restante."))
            ].spacing(12).into(),
            Surface::Context=>self.section("Fontes e validade","Contratos previstos para contexto incremental",column![
                self.notice("Índice indisponível","Nenhum arquivo do diretório foi indexado. Resultados futuros precisam de snapshot, origem, método e validade."),
                self.paragraph("Extração sintática, resolução semântica e inferência serão identificadas separadamente. Similaridade não comprova uma chamada entre símbolos."),
                self.unavailable("Consultar contexto · não integrado")
            ].spacing(12).into()),
            Surface::Providers=>self.section("Provedores e modelos","Conexão exige escopo de transmissão e autorização",column![
                self.notice("Nenhum provedor integrado","Não há envio de código, credenciais ou solicitações a modelos nesta interface."),
                self.paragraph("A configuração futura mostrará disponibilidade, capacidades e dados potencialmente transmitidos. Preço e limites só serão exibidos com fonte e período."),
                self.unavailable("Conectar provedor · não integrado")
            ].spacing(12).into()),
            Surface::Tools=>self.section("Plugin Host e ferramentas","Fundação disponível como API independente",column![
                self.notice("Host ainda não conectado ao desktop","O contrato local de plugins possui negociação e ciclo de vida. Um manifesto não comprova isolamento do sistema operacional."),
                self.paragraph("LSP e serviços avançados serão opcionais via plugins. Navegar nesta tela não inicia processos."),
                self.unavailable("Gerenciar plugins · não integrado")
            ].spacing(12).into()),
            Surface::Decisions=>self.section("Caixa de decisões","Solicitação → consequência → resposta → confirmação",column![
                self.notice("Nenhuma caixa de decisões integrada","A tela não deduz permissões a partir de arquivos, planos, skills ou silêncio do usuário."),
                self.paragraph("Cada decisão futura terá escopo, identidade, validade e consequência. Solicitar, responder e aplicar são etapas distintas."),
                self.unavailable("Responder decisão · não integrado")
            ].spacing(12).into()),
            Surface::Sdd=>self.section("Artefatos portáveis","Arquivos são a autoridade; não há parser integrado ao desktop",column![
                self.notice("spec.md","Requisitos, atores, invariantes e critérios de aceitação."),
                self.notice("plan.md / tasks.md","Decisões e riscos, métodos consultados, dependências e trabalho verificável."),
                self.notice("traceability.json / evidence.json","Vínculo entre critério, implementação, oráculo e observação; hashes não substituem avaliação semântica."),
                self.unavailable("Abrir SDD do projeto · não integrado")
            ].spacing(12).into()),
            Surface::Skills=>self.section("Descoberta e uso de competências","Biblioteca do repositório e skills do projeto do usuário são contextos distintos",column![
                self.notice("Disponível → indicada → selecionada → consultada → usada","Nenhuma dessas etapas concede autorização de execução ou prova aceitação do produto."),
                self.paragraph("A biblioteca do Ox orienta este desenvolvimento. O carregamento e o registro de skills de projetos do usuário ainda não estão integrados ao aplicativo."),
                self.unavailable("Carregar skills do projeto · não integrado")
            ].spacing(12).into()),
            _=>self.unavailable("Operação não integrada"),
        };
        body
    }
    fn content(&self) -> Element<'_, Message> {
        if self.surface == Surface::Start {
            return self.start_view();
        }
        if self.surface == Surface::NewProject {
            return self.new_project_view();
        }
        if matches!(self.surface, Surface::Editor | Surface::Focus) {
            return column![
                text(self.surface.title()).font(HEADING_FONT).size(20),
                self.document_view()
            ]
            .spacing(self.density.gap())
            .into();
        }
        let p = self.appearance.palette();
        let mut body = column![
            row![
                text(format!(
                    "{}  /  {}",
                    self.surface.group(),
                    self.surface.code()
                ))
                .size(12)
                .color(p.text_muted),
                space::horizontal(),
                self.badge()
            ]
            .spacing(12)
            .wrap(),
            text(self.surface.title()).font(HEADING_FONT).size(24),
            self.paragraph(self.surface.summary()),
            self.notice(self.surface.backend(), self.surface.dependency())
        ]
        .spacing(self.density.gap());
        if let Some(error) = &self.history_error {
            body = body.push(self.notice("Histórico de projetos", error.as_str()));
        }
        let contents:Element<'_,Message>=match self.surface {
            Surface::Start=>self.start_view(),
            Surface::Project=>column![self.workspace(),self.section("Capacidades do projeto","Disponibilidade real, sem inferir indexação ou agentes",self.notice("Fundação local","Tarefa controlada, supervisão e verificação independente. Editor, agentes de IA, contexto, grafos e persistência têm integração própria pendente."))].spacing(12).into(),
            Surface::NewProject=>self.new_project_view(),
            Surface::Tasks=>column![self.workspace(),self.task_actions(),self.evidence()].spacing(self.density.gap()).into(),
            Surface::NewTask=>self.section("Intenção da tarefa","Rascunho de apresentação · preservado apenas nesta sessão",column![
                text("Objetivo e restrições").size(14),Self::tracked_input(text_input("Descreva o resultado esperado",&self.draft).id("task-draft").size(15).padding(10).on_input(Message::Draft).on_submit(Message::InputFocused(230)),230),
                self.notice("Contexto e plano","O planejador futuro deverá explicitar fontes, critérios e consequências antes da execução."),
                self.unavailable("Planejar tarefa · não integrado")
            ].spacing(12).into()),
            Surface::Activity|Surface::Trace|Surface::Tests=>column![
                self.section(if self.surface==Surface::Tests{"Oráculo local"}else{"Tentativa e observações"},"Informação do Controller atual; não é streaming de logs",self.notice("Verificação independente","O produtor grava o candidato e o oráculo compara identidade e conteúdo. Atualizar inputs reavalia a atualidade sem executar o oráculo.")),self.evidence()
            ].spacing(12).into(),
            Surface::Settings|Surface::Appearance=>self.appearance_view(),
            Surface::Editor|Surface::Focus=>self.document_view(),
            Surface::Architecture=>self.architecture_view(),
            Surface::Observability=>self.observability_view(),
            Surface::Review=>self.review_view(),
            Surface::Recovery=>column![self.section("Efeitos e recuperação","Cancelamento não significa reversão",self.notice("Preservação primeiro","Os arquivos exclusivos de tentativa permanecem no diretório. Sem serviço de recuperação, esta tela não oferece rollback nem garante desfazer efeitos.")),self.evidence()].spacing(12).into(),
            Surface::Problems=>self.section("Diagnósticos","Origem e severidade são necessárias",column![self.notice("Sem provedor de diagnósticos","Não há análise LSP conectada. Ausência de dados não significa ausência de problemas no projeto."),self.unavailable("Inspecionar diagnóstico · não integrado")].spacing(12).into()),
            Surface::Terminal=>self.section("Saída do processo","Captura bruta e compactação têm contratos próprios",column![self.notice("Terminal não integrado","O cenário controlado não captura stdout/stderr. Não há shell arbitrário ou saída fictícia nesta tela."),self.unavailable("Abrir terminal · não integrado")].spacing(12).into()),
            _=>self.capability_view(),
        };
        if self.details {
            body=body.push(self.notice("Limites desta execução","Processos locais controlados, sem sandbox, agentes remotos ou histórico persistente de tarefas. A interface representa capacidades previstas separadamente das integrações reais."));
        }
        body.push(contents).into()
    }
    fn navigation(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let mut items = column![
            text("EXPLORAR A BANCADA")
                .font(HEADING_FONT)
                .size(12)
                .color(p.text_muted)
        ]
        .spacing(4);
        let mut group = "";
        for surface in Surface::ALL {
            if surface.group() != group {
                group = surface.group();
                items = items
                    .push(container(text(group).size(11).color(p.text_muted)).padding([12, 8]));
            }
            let button = self
                .styled_control(
                    surface.id(),
                    surface.title(),
                    Some(Message::Navigate(surface)),
                    ButtonRole::Navigation(self.surface == surface),
                )
                .width(Length::Fill);
            items = items.push(button);
        }
        container(column![
            container(
                column![
                    text("OX WORKBENCH").size(13).font(HEADING_FONT),
                    text(if self.selected {
                        "Projeto local validado"
                    } else {
                        "Nenhum projeto selecionado"
                    })
                    .size(12)
                    .color(p.text_muted)
                ]
                .spacing(5)
            )
            .padding(12),
            rule::horizontal(1),
            scrollable(items.padding(8))
                .id("navigation")
                .height(Length::Fill),
            container(
                text("Local-first · Rust / Iced")
                    .size(12)
                    .color(p.text_muted)
            )
            .padding(12)
        ])
        .width(if self.width < 980.0 {
            Length::Fill
        } else {
            Length::Fixed(232.0)
        })
        .height(Length::Fill)
        .style(move |_| container::Style {
            background: Some(p.explorer_bg.into()),
            text_color: Some(p.text_primary),
            ..Default::default()
        })
        .into()
    }
    fn command_palette(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let mut results = column![].spacing(4);
        for (i, surface) in self.command_matches().into_iter().enumerate() {
            results = results.push(
                self.styled_control(
                    surface.id(),
                    surface.title(),
                    Some(Message::Navigate(surface)),
                    ButtonRole::Navigation(self.command_selection == i),
                )
                .width(Length::Fill),
            );
        }
        if self.command_matches().is_empty() {
            results = results.push(
                self.paragraph("Nenhuma tela encontrada. Tente um nome ou código, como S04."),
            );
        }
        container(
            column![
                row![
                    text("Ir para uma tela").size(22).font(HEADING_FONT),
                    space::horizontal(),
                    self.control(301, "Fechar · Esc", Some(Message::Escape))
                ]
                .spacing(12)
                .wrap(),
                self.paragraph("Busque pelo nome ou código. Enter abre o resultado selecionado."),
                Self::tracked_input(
                    text_input("Tarefas, arquitetura, S04…", &self.command)
                        .id("command")
                        .size(16)
                        .padding(12)
                        .on_input(Message::CommandInput)
                        .on_submit(Message::CommandGo),
                    300
                ),
                scrollable(results).height(Length::Fill)
            ]
            .spacing(16),
        )
        .padding(24)
        .max_width(760)
        .height(Length::Fill)
        .style(move |_| design::panel(p.surface_base, p.text_primary, p.border_decorative))
        .into()
    }
    #[expect(
        clippy::too_many_lines,
        reason = "Top-level widget tree composes header, navigation, main panel and footer"
    )]
    pub(super) fn view(&self) -> Element<'_, Message> {
        if self.entry() && !self.command_open {
            return self.welcome_view();
        }
        let p = self.appearance.palette();
        let context = if self.selected {
            "Projeto local"
        } else {
            "Selecione um projeto"
        };
        let chrome = container(
            row![
                self.styled_control(
                    212,
                    if self.navigation_open {
                        "☰ Ocultar navegação"
                    } else {
                        "☰ Navegação"
                    },
                    Some(Message::Navigation),
                    ButtonRole::Chrome
                ),
                text("Ox").font(HEADING_FONT).size(24),
                text(context).size(13),
                space::horizontal(),
                text("LOCAL").size(12)
            ]
            .spacing(14)
            .align_y(Alignment::Center),
        )
        .padding([8, 12])
        .width(Length::Fill)
        .style(move |_| container::Style {
            background: Some(p.shell_bg.into()),
            text_color: Some(p.text_shell),
            ..Default::default()
        });
        let mut tools = row![
            self.styled_control(
                213,
                "Ir para…  Ctrl+K",
                Some(Message::Command),
                ButtonRole::Secondary
            ),
            self.control(
                210,
                if self.width < 980.0 {
                    "Tema"
                } else {
                    self.appearance.label()
                },
                Some(Message::CycleAppearance)
            ),
            self.control(211, self.density.label(), Some(Message::CycleDensity)),
            self.control(
                0,
                if self.details {
                    "Ocultar detalhes"
                } else {
                    "Detalhes"
                },
                Some(Message::Toggle)
            ),
            self.control(1, "Sair", Some(Message::Close))
        ];
        // On the entry screen, an idle cancellation affordance only consumes
        // space needed by the folder form at the minimum supported window size.
        if self.busy || self.surface != Surface::Start {
            tools = tools.push(self.styled_control(
                214,
                "Cancelar operação",
                self.busy.then_some(Message::Cancel),
                ButtonRole::Danger,
            ));
        }
        let toolbar = container(tools.spacing(8).wrap())
            .padding([8, 12])
            .width(Length::Fill)
            .style(move |_| container::Style {
                background: Some(p.surface_recessed.into()),
                text_color: Some(p.text_primary),
                ..Default::default()
            });
        let center: Element<'_, Message> = if self.command_open {
            container(self.command_palette())
                .padding(self.density.inset())
                .center_x(Length::Fill)
                .height(Length::Fill)
                .into()
        } else {
            let main_panel = scrollable(
                container(self.content())
                    .width(Length::Fill)
                    .max_width(1320)
                    .padding(self.density.inset()),
            )
            .id("main")
            .width(Length::Fill)
            .height(Length::Fill);
            if self.navigation_open {
                if self.width < 980.0 {
                    self.navigation()
                } else {
                    row![self.navigation(), main_panel]
                        .height(Length::Fill)
                        .into()
                }
            } else {
                main_panel.into()
            }
        };
        let footer = container(
            row![
                text(if self.busy {
                    "◌ Operação em andamento"
                } else {
                    "• Sessão local"
                })
                .size(12),
                space::horizontal(),
                text(format!(
                    "{} · {} · tarefas nesta sessão",
                    self.surface.code(),
                    self.density.label()
                ))
                .size(12)
            ]
            .spacing(8)
            .wrap(),
        )
        .padding([6, 12])
        .width(Length::Fill)
        .style(move |_| container::Style {
            background: Some(p.shell_deep.into()),
            text_color: Some(p.text_shell),
            ..Default::default()
        });
        container(column![chrome, toolbar, center, footer].height(Length::Fill))
            .height(Length::Fill)
            .width(Length::Fill)
            .style(move |_| container::Style {
                background: Some(p.workbench_bg.into()),
                text_color: Some(p.text_primary),
                ..Default::default()
            })
            .into()
    }
}
