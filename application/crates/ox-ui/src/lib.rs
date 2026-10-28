//! Minimal desktop shell; no agents or plugins are started.
#![forbid(unsafe_code)]

mod desktop;
pub mod shell;
pub use desktop::{Result, run};
