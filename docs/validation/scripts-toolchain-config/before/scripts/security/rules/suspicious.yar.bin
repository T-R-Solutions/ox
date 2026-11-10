// SPDX-License-Identifier: MIT
// Indicators require human investigation. Matches are not proof of malicious intent.
rule download_and_execute {
  meta:
    description = "Network downloader combined with shell execution"
  strings:
    $curl = "curl " ascii
    $wget = "wget " ascii
    $shell = /\|[ \t]*(ba)?sh([ \t\r\n]|$)/
  condition:
    ($curl or $wget) and $shell
}
rule encoded_powershell {
  meta:
    description = "PowerShell encoded command requires review"
  strings:
    $ps = "powershell" nocase ascii
    $enc = "-EncodedCommand" nocase ascii
  condition:
    $ps and $enc
}
