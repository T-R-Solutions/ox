pub type Result = ox_ui::Result;

/// Start the desktop runtime and propagate initialization failures.
pub fn run() -> Result {
    ox_ui::run()
}
