# Plugin Host acceptance review

AC-01/06: real_process_negotiation_shutdown_and_recovery launches compiled local-plugin, echoes two correlated requests, checks terminal admission, removes owned socket directory after drop and starts a new host.
AC-02/03: incompatible_and_unauthorized_are_rejected rejects major 2. Fixture exits 21 on any unauthorized CALL, so successful STOP independently proves denied CALL was not delivered. Unsupported capability also denies despite grant.
AC-04: malformed_oversized_and_wrong_correlation_fail_closed rejects malformed text, >1024-byte frame and wrong id; further calls fail after terminal error.
AC-05: timeout_and_crash_are_distinct_and_bounded observes separate Timeout/UnexpectedExit with <3-second wall bound for 300ms configured response deadline.
Compilation, format and Clippy pass; socket test requires host socket access denied by the execution sandbox. Approved rerun passed.
Protocol uses a private 0700 local socket directory, trusted fixture executable and strict ASCII framing, not JSON-RPC/ACP. No host-mediated filesystem operations exist; the process retains its OS permissions.

