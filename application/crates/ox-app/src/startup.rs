pub type Result = ox_ui::Result;

/// Start the desktop runtime and propagate initialization failures.
/// # Errors
/// Returns the native desktop initialization or event-loop error.
pub fn run() -> Result {
    ox_ui::run()
}
