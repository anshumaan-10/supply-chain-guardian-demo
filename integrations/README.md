# 🔌 Integration Examples

> Run **Supply Chain Guardian** anywhere — not just GitHub Actions.

## GitHub Actions (Native)

SCG is a GitHub Actions composite action. See the main [showcase pipeline](../.github/workflows/showcase-pipeline.yml) for the full 8-job demo.

```yaml
- uses: anshumaan-10/supply-chain-guardian@v4
  with:
    scan-mode: deep
    fail-on-severity: high
    verbose: true
```

## GitLab CI

[`.gitlab-ci.yml`](.gitlab-ci.yml) — Drop-in template for any GitLab project.

```yaml
# Highlights:
stages: [scan, build, test, deploy]

supply-chain-scan:
  stage: scan
  image: python:3.11-slim
  script:
    - git clone --depth 1 https://github.com/anshumaan-10/supply-chain-guardian.git /opt/scg
    - INPUT_SCAN_MODE=deep python /opt/scg/src/main.py --workspace "$CI_PROJECT_DIR"
  artifacts:
    reports:
      sast: supply-chain-guardian.sarif    # ← GitLab Security Dashboard
```

**Key features:**
- SARIF report feeds directly into GitLab's Security Dashboard
- Pre-build gate — pipeline fails if threats exceed threshold
- Works with shared runners, no special plugins required

## Jenkins

[`Jenkinsfile`](Jenkinsfile) — Declarative pipeline with SCG as a build gate.

```groovy
stage('Supply Chain Scan') {
    steps {
        sh '''
            git clone --depth 1 https://github.com/anshumaan-10/supply-chain-guardian.git /tmp/scg
            INPUT_SCAN_MODE=deep python3 /tmp/scg/src/main.py --workspace "${WORKSPACE}"
        '''
    }
    post {
        always {
            recordIssues(tools: [sarif(pattern: 'supply-chain-guardian.sarif')])
        }
    }
}
```

**Key features:**
- SARIF integration with `warnings-ng` plugin
- Build artifacts archived automatically
- ANSI color output in Jenkins console

## Local CLI

[`local-cli-scan.sh`](local-cli-scan.sh) — Run SCG from any developer machine.

```bash
# Install and scan current directory
./local-cli-scan.sh

# Paranoid scan with HTML report
./local-cli-scan.sh --mode paranoid --html report.html /path/to/project

# Quick scan, quiet mode
./local-cli-scan.sh --mode quick --quiet .
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `--mode <mode>` | `quick`, `deep`, or `paranoid` | `deep` |
| `--fail <level>` | `low`, `medium`, `high`, `critical` | `high` |
| `--html <path>` | Generate HTML report | — |
| `--json <path>` | Generate JSON report | — |
| `--sarif` | Generate SARIF output | off |
| `--quiet` | Reduce verbosity | off |
| `--update` | Force re-download SCG | off |

## Azure DevOps

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.11'

  - script: |
      pip install pyyaml requests tabulate colorama jsonschema semver
      git clone --depth 1 https://github.com/anshumaan-10/supply-chain-guardian.git /tmp/scg
      INPUT_SCAN_MODE=deep \
      INPUT_FAIL_ON_SEVERITY=high \
      INPUT_VERBOSE=true \
      INPUT_SARIF_OUTPUT=true \
      python /tmp/scg/src/main.py --workspace "$(Build.SourcesDirectory)"
    displayName: 'Supply Chain Guardian Scan'

  - task: PublishBuildArtifacts@1
    inputs:
      PathtoPublish: 'supply-chain-guardian.sarif'
      ArtifactName: 'security-reports'
```

## CircleCI

```yaml
# .circleci/config.yml
version: 2.1

jobs:
  supply-chain-scan:
    docker:
      - image: python:3.11-slim
    steps:
      - checkout
      - run:
          name: Install SCG
          command: |
            pip install pyyaml requests tabulate colorama jsonschema semver
            git clone --depth 1 https://github.com/anshumaan-10/supply-chain-guardian.git /tmp/scg
      - run:
          name: Run Scan
          command: |
            INPUT_SCAN_MODE=deep \
            INPUT_FAIL_ON_SEVERITY=high \
            INPUT_VERBOSE=true \
            python /tmp/scg/src/main.py --workspace "$PWD"
      - store_artifacts:
          path: supply-chain-guardian.sarif

workflows:
  security:
    jobs:
      - supply-chain-scan
```

---

## Environment Variables Reference

All SCG inputs can be passed as environment variables with the `INPUT_` prefix:

| Variable | Description |
|----------|-------------|
| `INPUT_SCAN_MODE` | `quick`, `deep`, or `paranoid` |
| `INPUT_FAIL_ON_SEVERITY` | `low`, `medium`, `high`, `critical`, or `none` |
| `INPUT_VERBOSE` | `true` or `false` |
| `INPUT_JSON_OUTPUT` | Path for JSON report |
| `INPUT_HTML_OUTPUT` | `true` to enable HTML report |
| `INPUT_HTML_OUTPUT_PATH` | Path for HTML report file |
| `INPUT_SARIF_OUTPUT` | `true` to generate SARIF |
| `INPUT_SCAN_BINARIES` | `true` to enable binary analysis |
| `INPUT_EXCEPTION_CONFIG` | Path to `.scg-config.yml` |
| `INPUT_EGRESS_ALLOWLIST` | Comma-separated allowed domains |

---

<sub>Copyright (c) 2025-2026 Anshumaan Singh. All rights reserved.</sub>
