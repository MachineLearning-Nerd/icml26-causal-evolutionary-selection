# Branch and attribution audit

## Target policy

- Canonical branch: main
- Intended branch count after migration: one
- Legacy collection anchor: mOcTXKawFY
- Repository owner: MachineLearning-Nerd

## Branch purpose

The repository contains one clean-room audit. No experimental or OpenResearch
branch is part of the published workflow. The verifier and publication gate
are the source of truth for the bounded evidence status.

## Commit identity

Reachable audit commits are expected to use:

~~~text
Name:  MachineLearning-Nerd
Email: 37579156+MachineLearning-Nerd@users.noreply.github.com
~~~

No co-author or tool-attribution trailers are part of the audit history.

## Migration record

The original collection repository used a master branch and a generated
reproduction commit. The cleanup renames the repository to
icml26-causal-evolutionary-selection, normalizes the branch to main, removes
the legacy remote branch, and rewrites reachable commit attribution to the
MachineLearning-Nerd identity. The final remote branch list and commit tips
must be checked after publication.

## Live verification

The final remote audit confirmed repository name `icml26-causal-evolutionary-selection`, default branch `main`, sole remote branch `main`, canonical paper homepage, README and gate publication, and MachineLearning-Nerd as both author and committer on all reachable commits.
