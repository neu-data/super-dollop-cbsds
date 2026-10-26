# Export .pptx and .docx files to PDF using installed Microsoft Office (instructor build step).
# Usage: powershell -ExecutionPolicy Bypass -File build/export_office.ps1 <file1> <file2> ...
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Files)

foreach ($f in $Files) {
    $full = (Resolve-Path $f).Path
    $pdf = [System.IO.Path]::ChangeExtension($full, ".pdf")
    if ($full -like "*.pptx") {
        $app = New-Object -ComObject PowerPoint.Application
        $pres = $app.Presentations.Open($full, $true, $false, $false)
        $pres.SaveAs($pdf, 32)   # ppSaveAsPDF
        $pres.Close(); $app.Quit()
    } elseif ($full -like "*.docx") {
        $app = New-Object -ComObject Word.Application
        $app.Visible = $false
        $doc = $app.Documents.Open($full, $false, $true)
        $doc.SaveAs([ref]$pdf, [ref]17)   # wdFormatPDF
        $doc.Close([ref]$false); $app.Quit()
    }
    Write-Output "Exported $pdf"
}
