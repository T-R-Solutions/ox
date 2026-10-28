# Mediated permissions and containment

For each effect, list whether it passes through the host or is available directly to the plugin process. Test both paths. Capability checks protect the first; OS/container/runtime controls are needed for the second. A process boundary contains some crashes but does not revoke the user's filesystem or network permissions.

Bind grants to identity, instance, resource scope, operation and lifetime. Recheck revocation at the effect boundary, not only at handshake. Normalize and constrain file handles using mechanisms supported by the target platform; a string prefix comparison is insufficient for paths.

Use an isolated disposable directory with an allowed file and a denied sentinel. Observe sentinel content and access outcome after the denied operation. A mock returning permission_denied cannot establish that a native process could not bypass IPC. If the OS mechanism is undecided, deliver a threat/control matrix with that cell unverified. Authentication, signatures and containment answer different questions.
