param(
  [Parameter(Mandatory=$true)]
  [string]$MinerUToken,
  [Parameter(Mandatory=$true)]
  [string]$BatchId
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$mdDir = Join-Path $root "work\data\mineru_markdown"
$logDir = Join-Path $root "work\logs"
$logPath = Join-Path $logDir "mineru_batch_downloads.jsonl"
New-Item -ItemType Directory -Force -Path $mdDir, $logDir | Out-Null

$headers = @{ "Authorization" = "Bearer $MinerUToken"; "Accept" = "*/*" }

for ($round = 0; $round -lt 60; $round++) {
  Start-Sleep -Seconds 10
  $poll = Invoke-RestMethod -Uri "https://mineru.net/api/v4/extract-results/batch/$BatchId" -Method Get -Headers $headers -TimeoutSec 60
  $items = @($poll.data.extract_result)
  $doneOrFailed = 0
  $idx = 0
  foreach ($item in $items) {
    $idx += 1
    $record = [ordered]@{
      time = (Get-Date).ToString("s")
      batch_id = $BatchId
      index = $idx
      data_id = $item.data_id
      file_name = $item.file_name
      state = $item.state
      error = $item.err_msg
      saved_markdown = $null
    }
    if ($item.state -eq "done" -or $item.full_zip_url) {
      $doneOrFailed += 1
      $base = "batch_$($BatchId)_item_$idx"
      $zipPath = Join-Path $mdDir "$base.zip"
      $targetMd = Join-Path $mdDir "$base.md"
      if (-not (Test-Path $targetMd)) {
        Invoke-WebRequest -Uri $item.full_zip_url -OutFile $zipPath -Headers @{ "User-Agent" = "Mozilla/5.0" } -TimeoutSec 180
        $extractDir = Join-Path $mdDir $base
        New-Item -ItemType Directory -Force -Path $extractDir | Out-Null
        Expand-Archive -Path $zipPath -DestinationPath $extractDir -Force
        $fullMd = Get-ChildItem -Path $extractDir -Recurse -Filter "full.md" | Select-Object -First 1
        if ($fullMd) {
          Copy-Item -Path $fullMd.FullName -Destination $targetMd -Force
          $record.saved_markdown = $targetMd
        }
      } else {
        $record.saved_markdown = $targetMd
      }
    } elseif ($item.state -eq "failed") {
      $doneOrFailed += 1
    }
    ($record | ConvertTo-Json -Compress -Depth 5) | Add-Content -Path $logPath -Encoding UTF8
  }
  if ($items.Count -gt 0 -and $doneOrFailed -ge $items.Count) {
    break
  }
}

Write-Output "markdown dir: $mdDir"
Write-Output "log: $logPath"
