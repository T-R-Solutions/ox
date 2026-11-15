use std::path::{Path, PathBuf};
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WorkspaceRoot(PathBuf);
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RelativeRoot;
impl WorkspaceRoot {
    /// # Errors
    /// Returns `RelativeRoot` when `path` is not absolute.
    pub fn new(path: PathBuf) -> Result<Self, RelativeRoot> {
        if path.is_absolute() {
            Ok(Self(path))
        } else {
            Err(RelativeRoot)
        }
    }
    #[must_use]
    pub fn path(&self) -> &Path {
        &self.0
    }
}
