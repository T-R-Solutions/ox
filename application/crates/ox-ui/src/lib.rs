//! Native visual workbench. Navigation never starts agents or plugins.
#![forbid(unsafe_code)]

pub mod design;
mod desktop;
pub mod shell;
pub mod tokens;
pub mod workbench;
pub use desktop::{Result, run};

pub mod local_task;
