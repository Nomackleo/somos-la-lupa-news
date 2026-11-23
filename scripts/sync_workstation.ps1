<#
.SYNOPSIS
    Multi-Host Git Synchronization Helper for La Lupa News (Nomack Studio v5.0.0)
.DESCRIPTION
    Enforces Pre-Flight Fetch, Zero Data Loss, ISO 27001 secret guard (.secrets/ never staged),
    and synchronized push/pull between Desktop (HOST-01-STUDIO) and Laptop Nitro (HOST-02-MOBILE).
.EXAMPLE
    .\scripts\sync_workstation.ps1 -Action status
    .\scripts\sync_workstation.ps1 -Action pull
    .\scripts\sync_workstation.ps1 -Action push
#>
[CmdletBinding()]
param(
    [ValidateSet("status", "pull", "push")]
    [string]$Action = "status",
    [string]$Branch = "main"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$HostId = $env:NOMACK_STUDIO_HOST_ID
if ([string]::IsNullOrWhiteSpace($HostId)) {
    $HostId = "UNSET ($env:COMPUTERNAME)"
}

function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]]$GitArgs)
    $out = & git -C $RepoRoot @GitArgs 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "git $($GitArgs -join ' ') failed: $out"
    }
    return $out
}

# ISO 27001 Pre-Check: verify .secrets/ is never tracked or staged
$trackedSecrets = & git -C $RepoRoot ls-files ".secrets"
if ($trackedSecrets) {
    throw "[ISO 27001 CRITICAL] Files inside .secrets/ are tracked by Git! Abort immediately."
}

# Phase 1: Pre-Flight Fetch
Invoke-Git @("fetch", "origin", "--prune") | Out-Null
$counts = (Invoke-Git @("rev-list", "--left-right", "--count", "HEAD...origin/$Branch")).Trim() -split "\s+"
$localAhead = [int]$counts[0]
$remoteAhead = [int]$counts[1]
$dirty = (& git -C $RepoRoot status --porcelain)
$workingState = if ($dirty) { "DIRTY" } else { "CLEAN" }

$remoteState = if ($localAhead -eq 0 -and $remoteAhead -eq 0) {
    "IN_SYNC"
} elseif ($localAhead -eq 0 -and $remoteAhead -gt 0) {
    "REMOTE_AHEAD"
} elseif ($localAhead -gt 0 -and $remoteAhead -eq 0) {
    "LOCAL_AHEAD"
} else {
    "DIVERGED"
}

$executed = "NOOP"

if ($Action -eq "pull") {
    if ($remoteState -eq "REMOTE_AHEAD") {
        if ($workingState -eq "DIRTY") {
            $ts = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
            Invoke-Git @("stash", "push", "-u", "-m", "STASH_PRE_SYNC_${HostId}_${ts}") | Out-Null
            Invoke-Git @("pull", "--ff-only", "origin", $Branch) | Out-Null
            Invoke-Git @("stash", "pop") | Out-Null
            $executed = "STASH_FF_PULL_POP"
        } else {
            Invoke-Git @("pull", "--ff-only", "origin", $Branch) | Out-Null
            $executed = "FAST_FORWARD_PULL"
        }
    } elseif ($remoteState -eq "DIVERGED") {
        $ts = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
        $backupBranch = "backup/divergence-$($env:COMPUTERNAME)-$ts"
        Invoke-Git @("branch", $backupBranch) | Out-Null
        Invoke-Git @("pull", "--rebase", "--autostash", "origin", $Branch) | Out-Null
        $executed = "BACKUP_AND_REBASE ($backupBranch)"
    }
}
elseif ($Action -eq "push") {
    if ($remoteAhead -gt 0) {
        throw "Remote origin/$Branch is ahead by $remoteAhead commit(s). Run '-Action pull' first (Zero Data Loss)."
    }
    if ($localAhead -eq 0) {
        $executed = "NOOP_ALREADY_PUSHED"
    } else {
        Invoke-Git @("push", "origin", $Branch) | Out-Null
        $executed = "ATOMIC_PUSH"
    }
}

$headHash = (Invoke-Git @("rev-parse", "--short", "HEAD")).Trim()
$dirtyAfter = (& git -C $RepoRoot status --porcelain)
$workingStateAfter = if ($dirtyAfter) { "DIRTY" } else { "CLEAN" }

Write-Output ""
Write-Output "### Git Multi-Host Sync Telemetry (la-lupa-news)"
Write-Output "| Parametro | Valor Registrado |"
Write-Output "| :--- | :--- |"
Write-Output "| Host Activo | $HostId |"
Write-Output "| Proyecto / Repo | la-lupa-news (somos-la-lupa-news) |"
Write-Output "| Rama Local | $Branch |"
Write-Output "| Estado Remoto (GitHub) | $remoteState |"
Write-Output "| Delta Commits | Local: $localAhead | Remoto: $remoteAhead |"
Write-Output "| Accion Ejecutada | $executed |"
Write-Output "| Estado del Working Tree | $workingStateAfter |"
Write-Output "| Hash HEAD Sincronizado | $headHash |"
Write-Output ""
