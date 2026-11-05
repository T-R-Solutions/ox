#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ProtocolVersion {
    pub major: u16,
    pub minor: u16,
}
impl ProtocolVersion {
    /// A peer must share the major and provide at least the required minor.
    pub fn accepts(self, peer: Self) -> bool {
        self.major == peer.major && peer.minor >= self.minor
    }
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PluginDescriptor {
    pub name: String,
    pub protocol: ProtocolVersion,
    pub capabilities: Vec<String>,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum HostError {
    TransportUnavailable,
    IncompatibleVersion {
        required: ProtocolVersion,
        offered: ProtocolVersion,
    },
}
