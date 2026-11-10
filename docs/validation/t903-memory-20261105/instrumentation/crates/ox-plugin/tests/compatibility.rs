use ox_plugin::protocol::ProtocolVersion;
#[test]
fn reject_incompatible_peers() {
    let required = ProtocolVersion { major: 1, minor: 2 };
    assert!(!required.accepts(ProtocolVersion { major: 2, minor: 2 }));
    assert!(!required.accepts(ProtocolVersion { major: 1, minor: 1 }));
    assert!(required.accepts(required));
    assert!(required.accepts(ProtocolVersion { major: 1, minor: 3 }));
}
