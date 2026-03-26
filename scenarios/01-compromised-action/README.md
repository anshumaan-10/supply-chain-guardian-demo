# Scenario 01: Compromised GitHub Action

## Attack Vector
The `tj-actions/changed-files` action was compromised in March 2025 when attackers hijacked a Reviewdog
maintainer token and injected credential-stealing code into the action. Every CI job that used the
compromised commit SHA had its secrets exfiltrated to a remote server.

## What SCG Detects
| Finding | Severity | Rule |
|---------|----------|------|
| Known-bad SHA for tj-actions/changed-files | CRITICAL | SCA-001 |
| Compromised reviewdog action | CRITICAL | SCA-003 |
| Mutable tag reference (@v3 without SHA) | MEDIUM | SCA-007 |

## Vulnerable Code
```yaml
- uses: tj-actions/changed-files@ae82ed004850e9bfa8b2089b109a1e27e0eee893  # COMPROMISED
- uses: reviewdog/action-eslint@fff29c5  # COMPROMISED
- uses: actions/cache@v3  # MUTABLE TAG
```

## Remediation
- Always pin actions to full SHA: `actions/cache@1234567890abcdef...`
- Monitor [GitHub Advisory Database](https://github.com/advisories) for action compromises
- Use SCG in your CI pipeline to catch compromised SHAs automatically
