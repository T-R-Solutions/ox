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
    $enc = /-Encoded[C]ommand/ nocase ascii
  condition:
    $ps and $enc
}

// Assinatura do arquivo de teste antivírus EICAR. Não constitui catálogo universal de malware.
rule Ox_Eicar_Test_File {
    meta:
        description = "Detecta a assinatura de teste EICAR em arquivos analisados"
        reference = "https://www.eicar.org/download-anti-malware-testfile/"
    strings:
        $signature = /EICAR-STANDARD-ANTIVIRUS-TEST-FIL[E]/
    condition:
        $signature
}
