#[derive(Debug)]
pub enum StorageError {
    Unavailable,
    Io(std::io::Error),
    UnsupportedSchema { found: u32 },
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LocalStoreLocation(pub std::path::PathBuf);
