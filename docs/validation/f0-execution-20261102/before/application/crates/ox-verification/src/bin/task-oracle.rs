//! Independent task-result oracle; never writes candidate content.
#![forbid(unsafe_code)]
fn accepted() -> Option<bool> {
    let expected_identity = std::env::args().nth(1)?;
    let request = std::fs::read("request.txt").ok()?;
    let result = std::fs::read("result.txt").ok()?;
    let expected_request = format!("ox-task-v1:{expected_identity}\n");
    let expected_result = format!("{expected_request}result=42\n");
    Some(request == expected_request.as_bytes() && result == expected_result.as_bytes())
}
fn main() {
    if accepted() != Some(true) {
        std::process::exit(17);
    }
}
