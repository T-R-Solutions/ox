// Fault-injection model of the archived cancellation branch, not real OS faults.
use std::io;
#[derive(Default)]
struct Fake { calls: Vec<&'static str> }
impl Fake {
    fn kill(&mut self) -> io::Result<()> { self.calls.push("kill"); Err(io::Error::other("kill injected")) }
    fn try_wait(&mut self) -> io::Result<Option<()>> { self.calls.push("try_wait"); Err(io::Error::other("poll injected")) }
    fn wait(&mut self) -> io::Result<()> { self.calls.push("wait"); Ok(()) }
}
fn archived_cancel(child: &mut Fake) -> io::Result<()> {
    if let Err(error) = child.kill() && child.try_wait()?.is_none() { return Err(error); }
    child.wait()?;
    Ok(())
}
fn main() {
    let mut child = Fake::default();
    let result = archived_cancel(&mut child).unwrap_err();
    println!("injected kill error followed by injected try_wait error: {result}; calls={:?}; wait omitted, original kill error lost", child.calls);
    assert_eq!(child.calls, ["kill", "try_wait"]);
    assert_eq!(result.to_string(), "poll injected");
}
