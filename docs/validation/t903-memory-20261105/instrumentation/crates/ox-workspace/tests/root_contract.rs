use ox_workspace::root::WorkspaceRoot;
#[test]
fn requires_absolute_path_without_claiming_existence() {
    assert!(WorkspaceRoot::new("relative".into()).is_err());
    assert!(WorkspaceRoot::new("/not-required-to-exist/文".into()).is_ok());
}
