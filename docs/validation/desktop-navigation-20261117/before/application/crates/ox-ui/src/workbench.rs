//! Navigation and integration contracts for current and planned native surfaces.

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub enum Surface {
    #[default]
    Start,
    NewProject,
    Project,
    Tasks,
    NewTask,
    Activity,
    Decisions,
    Agents,
    AgentSettings,
    Providers,
    Context,
    Tools,
    Settings,
    Appearance,
    Editor,
    Architecture,
    Orchestration,
    Observability,
    Review,
    Recovery,
    Focus,
    Problems,
    Tests,
    Trace,
    Terminal,
    Sdd,
    Skills,
}

impl Surface {
    pub const ALL: [Self; 27] = [
        Self::Start,
        Self::NewProject,
        Self::Project,
        Self::Tasks,
        Self::NewTask,
        Self::Activity,
        Self::Decisions,
        Self::Agents,
        Self::AgentSettings,
        Self::Providers,
        Self::Context,
        Self::Tools,
        Self::Settings,
        Self::Appearance,
        Self::Editor,
        Self::Architecture,
        Self::Orchestration,
        Self::Observability,
        Self::Review,
        Self::Recovery,
        Self::Focus,
        Self::Problems,
        Self::Tests,
        Self::Trace,
        Self::Terminal,
        Self::Sdd,
        Self::Skills,
    ];
    #[must_use]
    /// # Panics
    /// Panics if the internal ALL table omits a Surface variant.
    pub fn index(self) -> usize {
        Self::ALL
            .iter()
            .position(|s| *s == self)
            .expect("Surface belongs to ALL")
    }
    #[must_use]
    pub fn id(self) -> usize {
        100 + self.index()
    }
    #[must_use]
    pub const fn code(self) -> &'static str {
        match self {
            Self::Start => "S01",
            Self::NewProject => "S02",
            Self::Project => "S03",
            Self::Tasks => "S04",
            Self::NewTask => "S05",
            Self::Activity => "S06",
            Self::Decisions => "S07",
            Self::Agents => "S08",
            Self::AgentSettings => "S09",
            Self::Providers => "S10",
            Self::Context => "S11",
            Self::Tools => "S12",
            Self::Settings => "S13",
            Self::Appearance => "S14",
            Self::Editor => "W00",
            Self::Architecture => "A01",
            Self::Orchestration => "A02",
            Self::Observability => "A03",
            Self::Review => "A04",
            Self::Recovery => "A05",
            Self::Focus => "A06",
            Self::Problems => "TW01",
            Self::Tests => "TW02",
            Self::Trace => "TW03",
            Self::Terminal => "TW04",
            Self::Sdd => "SDD",
            Self::Skills => "SKL",
        }
    }
    #[must_use]
    pub const fn title(self) -> &'static str {
        match self {
            Self::Start => "Boas-vindas",
            Self::NewProject => "Novo projeto",
            Self::Project => "Visão do projeto",
            Self::Tasks => "Tarefas",
            Self::NewTask => "Criar tarefa",
            Self::Activity => "Atividade e evidências",
            Self::Decisions => "Decisões e permissões",
            Self::Agents => "Agentes",
            Self::AgentSettings => "Configurar agente",
            Self::Providers => "Modelos e provedores",
            Self::Context => "Contexto e conhecimento",
            Self::Tools => "Ferramentas e plugins",
            Self::Settings => "Preferências",
            Self::Appearance => "Aparência",
            Self::Editor => "Editor e arquivos",
            Self::Architecture => "Arquitetura",
            Self::Orchestration => "Orquestração",
            Self::Observability => "Observabilidade",
            Self::Review => "Revisão de alterações",
            Self::Recovery => "Falhas e recuperação",
            Self::Focus => "Modo de foco",
            Self::Problems => "Problemas",
            Self::Tests => "Testes",
            Self::Trace => "Rastro de execução",
            Self::Terminal => "Terminal",
            Self::Sdd => "Desenvolvimento SDD",
            Self::Skills => "Skills do projeto",
        }
    }
    #[must_use]
    pub const fn group(self) -> &'static str {
        match self {
            Self::Start | Self::NewProject | Self::Project => "PROJETO",
            Self::Tasks | Self::NewTask | Self::Activity | Self::Decisions => "TRABALHO",
            Self::Agents
            | Self::AgentSettings
            | Self::Providers
            | Self::Context
            | Self::Tools
            | Self::Orchestration => "CAPACIDADES",
            Self::Settings | Self::Appearance => "PREFERÊNCIAS",
            _ => "BANCADA",
        }
    }
    #[must_use]
    pub const fn summary(self) -> &'static str {
        match self {
            Self::Start => "Abra uma pasta, crie um projeto vazio ou retome um projeto recente.",
            Self::NewProject => "Crie uma pasta vazia em um destino confirmado e abra o projeto.",
            Self::Project => {
                "O diretório validado organiza tarefas, artefatos e capacidades disponíveis."
            }
            Self::Tasks => {
                "Execute um cenário controlado. Verifique o resultado em uma etapa independente."
            }
            Self::NewTask => {
                "Defina intenção, contexto e restrições antes do planejamento e da execução."
            }
            Self::Activity => {
                "Cada observação tem critério, tentativa, inputs e atualidade próprios."
            }
            Self::Decisions => {
                "Uma solicitação não é uma confirmação; uma decisão não executa uma operação."
            }
            Self::Agents => {
                "Definições descrevem papéis. Instâncias pertencem a uma execução identificada."
            }
            Self::AgentSettings => {
                "Capacidades, modelo e permissões precisam de contratos e escopo explícitos."
            }
            Self::Providers => {
                "Disponibilidade, origem e dados transmitidos devem ser verificáveis."
            }
            Self::Context => {
                "Contexto exige origem, snapshot e validade; similaridade não é relação confirmada."
            }
            Self::Tools => "Extensões opcionais com contratos, capacidades e falhas explícitas.",
            Self::Settings => "Preferências de apresentação disponíveis nesta sessão.",
            Self::Appearance => {
                "Identidade azul, superfícies neutras e semântica consistente entre temas."
            }
            Self::Editor => "Área principal de inspeção de arquivos, código e alterações.",
            Self::Architecture => {
                "Modos estrutural e exploratório sobre o mesmo grafo lógico com proveniência."
            }
            Self::Orchestration => {
                "Dependências, tentativas e responsabilidades sem confundir atividade com sucesso."
            }
            Self::Observability => {
                "Valores medidos, derivados, estimados e indisponíveis permanecem distintos."
            }
            Self::Review => "Alteração, verificação técnica e aceite são decisões diferentes.",
            Self::Recovery => "Diagnóstico e efeitos conhecidos antes de escolher uma recuperação.",
            Self::Focus => {
                "Concentre-se na tarefa e no artefato; mantenha ferramentas acessíveis sob demanda."
            }
            Self::Problems => {
                "Diagnósticos com origem, localização e severidade; LSP será opcional via plugins."
            }
            Self::Tests => {
                "Resultados técnicos precisam de caso, método, origem e evidência atual."
            }
            Self::Trace => {
                "Eventos ordenados e correlacionados à tentativa, preservando incerteza e falhas."
            }
            Self::Terminal => {
                "Saída bruta e código de saída precisam ser preservados antes da compactação."
            }
            Self::Sdd => {
                "Arquivos portáveis são a autoridade: requisitos, plano, tarefas e evidências."
            }
            Self::Skills => {
                "Disponível, indicada, selecionada, consultada e usada são estados diferentes."
            }
        }
    }
    #[must_use]
    pub const fn backend(self) -> &'static str {
        match self {
            Self::Start | Self::NewProject => "Projetos locais · histórico recente persistido",
            Self::Project
            | Self::Tasks
            | Self::Activity
            | Self::Trace
            | Self::Tests
            | Self::Recovery => "Tarefa local integrada",
            Self::Settings | Self::Appearance => "Apresentação · somente nesta sessão",
            _ => "Interface prevista · backend não integrado",
        }
    }
    #[must_use]
    pub const fn dependency(self) -> &'static str {
        match self {
            Self::Start => {
                "Lista recente local; abrir valida o diretório sem executar tarefas. Histórico de tarefas permanece nesta sessão."
            }
            Self::NewProject => {
                "Criação exclusiva de uma pasta vazia; validação local e histórico de projetos recentes."
            }
            Self::NewTask => {
                "Planejador e contratos de tarefas gerais; o cenário controlado continua disponível em Tarefas."
            }
            Self::Decisions => {
                "Inbox de decisões com identidade, expiração, escopo e confirmação do efeito."
            }
            Self::Agents | Self::AgentSettings | Self::Orchestration => {
                "Adaptadores de agentes reais e orquestrador; a supervisão de processo local não é um agente de IA."
            }
            Self::Providers => {
                "Adaptador de provedor autorizado, política de transmissão e gestão de credenciais."
            }
            Self::Context => "Indexação incremental, snapshots e consultas com proveniência.",
            Self::Tools => "Integração do Plugin Host ao desktop; manifesto não comprova sandbox.",
            Self::Editor | Self::Focus => {
                "Serviço de documentos, abertura/edição e preservação de mudanças concorrentes."
            }
            Self::Architecture => "Motores de contexto/grafo e relações vinculadas ao snapshot.",
            Self::Observability => {
                "Coletores e ledger de uso com fonte, unidade e período; ausência não é zero."
            }
            Self::Review => {
                "Serviço de alterações/diff e decisão de aceite; o oráculo local já é independente."
            }
            Self::Problems => {
                "Provedor de diagnósticos opcional via plugins, sem processo semântico obrigatório."
            }
            Self::Terminal => {
                "Captura de stdout/stderr e projeções com perdas explícitas; não há shell arbitrário nesta entrega."
            }
            Self::Sdd => "Leitura/reconciliação dos arquivos SDD sem estado concorrente.",
            Self::Skills => {
                "Carregamento de referências e registro de uso de skills de projetos do usuário."
            }
            _ => {
                "Controller, Runtime e Verification Engine locais; histórico em memória, sem persistência ou sandbox."
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn every_surface_has_unique_identity_and_explicit_integration_boundary() {
        for (i, s) in Surface::ALL.iter().enumerate() {
            assert_eq!(s.index(), i);
            assert_ne!(s.title(), "");
            assert_ne!(s.dependency(), "");
            assert_eq!(
                Surface::ALL
                    .iter()
                    .filter(|other| other.code() == s.code())
                    .count(),
                1
            );
        }
    }
}
