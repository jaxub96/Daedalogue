git add .

if (git diff --cached --quiet) {
    Write-Host "No changes to save"
}
else {
    $message = Read-Host "Commit message"

    if ([string]::IsNullOrWhiteSpace($message)) {
        $message = "auto save"
    }

    git commit -m "$message $(Get-Date)"
    git push
}