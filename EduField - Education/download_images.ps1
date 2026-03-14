$url = "https://alameed.edu.iq/"
$html = Invoke-WebRequest -Uri $url -UseBasicParsing
$images = $html.Images.src | Where-Object { $_ -match "\.(jpg|png)$" } | Select-Object -Unique

$targetDir = "d:\web projects\al-ameed-tempelet\EduField - Education\edufield\default\assets\img"
$count = 1
foreach ($img in $images) {
    if ($count -gt 5) { break }
    
    $fullUrl = $img
    if ($img.StartsWith("/")) {
        $fullUrl = "https://alameed.edu.iq" + $img
    } elseif (-not $img.StartsWith("http")) {
        continue
    }

    try {
        $ext = [System.IO.Path]::GetExtension($fullUrl)
        $fileName = "alameed_download_$count$ext"
        $dest = Join-Path $targetDir $fileName
        Invoke-WebRequest -Uri $fullUrl -OutFile $dest -UseBasicParsing
        Write-Host "Downloaded $fileName"
        $count++
    } catch {
        Write-Host "Failed to download $fullUrl"
    }
}
