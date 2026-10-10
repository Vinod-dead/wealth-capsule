$today = Get-Date

if ($today.Day -eq 1) {
    Set-Location "$PSScriptRoot\..\.."
    & ".\.venv\Scripts\python.exe" -m app.jobs.run_scheduled
}
