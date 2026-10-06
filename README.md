# Gitar workshop: Boxoffice

Boxoffice is the ticketing API behind a small venue's website. Customers buy tickets, each ticket carries a QR code, and gate staff scan it at the door. In this workshop you open three pull requests in your own fork and watch [Gitar](https://gitar.ai), Sonar's AI code verification agent, review them, fix them, and merge one. Findings and fixes can differ a little between runs.

| Stage | What you'll see | Branch |
|---|---|---|
| 1 | An out-of-the-box review, then a fix from one comment | `stage-1` |
| 2 | How a short `.gitar/` instruction and rule change a review | `stage-2` |
| 3 | A failing CI run, diagnosed, fixed, and merged from one comment | `stage-3` |

## Before you start

You need a GitHub account where you can install a GitHub App. Sign in at [app.gitar.ai](https://app.gitar.ai) first and start the GitHub install from there. Installing from GitHub Marketplace while signed out leaves nothing connected. Your 14-day Pro trial starts when you connect GitHub.

## Setup (about 4 minutes)

Do these steps in order. CI and Gitar both need to be on before you open a pull request.

1. Fork this repo. **Uncheck "Copy the `main` branch only"**, then confirm your fork shows 4 branches.
   [SCREENSHOT: UI — fork dialog with "Copy the main branch only" unchecked]
2. In your fork, open the **Actions** tab and click **I understand my workflows, go ahead and enable them**.
3. In Gitar, open **Settings > Configuration**, grant Gitar access to your fork, and confirm the fork is listed.
4. Open the three pull requests with these links, replacing `<your-username>` (and the repo name, if you renamed your fork). Stage 3 goes first because its pipeline takes longest.
   - Stage 3: `https://github.com/<your-username>/aie-ny-workshop-gitar/compare/main...stage-3?expand=1`
   - Stage 1: `https://github.com/<your-username>/aie-ny-workshop-gitar/compare/main...stage-1?expand=1`
   - Stage 2: `https://github.com/<your-username>/aie-ny-workshop-gitar/compare/main...stage-2?expand=1`

   The title and description fill in automatically, so just click **Create pull request**. If you use **New pull request** instead, change **base repository** to your fork first, or the pull request goes to `sonar-samples`.
5. In Gitar's settings, leave **Auto-merge PRs after auto-approve** off. Stage 3 turns on auto-merge for one pull request with a command.

## Merge controls (Stage 3 only)

> Only Stage 3's automatic merge needs these settings. Stages 1 and 2 work without them. If you skip this section, you still see Gitar's diagnosis and fix commit in Stage 3, and the presenter shows the merge. A good time to do it is while Gitar reviews your Stage 1 pull request.

1. In your fork, open **Settings > General > Pull Requests** and check **Allow auto-merge**.
   [SCREENSHOT: UI — Settings > General > Pull Requests with Allow auto-merge checked]
2. Open **Settings > Rules > Rulesets > New ruleset > New branch ruleset** and fill it in like this. Leave every field not listed at its default.

   | Field | Value |
   |---|---|
   | Ruleset name | `require-tests` |
   | Enforcement status | **Active** |
   | Bypass list | Empty |
   | Target branches | **Add target > Include default branch** |
   | Restrict deletions | Checked (default) |
   | Block force pushes | Checked (default) |
   | Require a pull request before merging | Unchecked |
   | Require status checks to pass | Checked |
   | Require branches to be up to date before merging | Unchecked |
   | Status checks | **Add checks**, type `test`, select **test** (GitHub Actions) |

   Then click **Create**. If `test` doesn't show up in the search, run **Actions > Test > Run workflow** on `main` and search again. Instead of filling in the form, you can use **New ruleset > Import a ruleset** and upload `setup/ruleset-require-tests.json` from this repo.
   [SCREENSHOT: UI — ruleset target branches set to Include default branch]
   [SCREENSHOT: UI — status check picker with test (GitHub Actions) selected]
3. In Gitar's behavior settings, turn on **Auto-approve PRs based on code review**. Leave **Auto-merge PRs after auto-approve** off. If a merge method is selectable, choose **Squash**. Gitar arms auto-merge only after it approves, so you need auto-approve even though the ruleset doesn't require an approval.

## Stage 1: out-of-the-box review, then `gitar fix`

Read the diff while Gitar reviews it, which takes 2 to 5 minutes. Find Gitar's **Important** inline finding and reply `gitar fix` in its thread (ticking **Apply fix** in the comment does the same thing). When Gitar's commit lands, open it, look at which files it changed, and check that CI is green. Don't merge this pull request.

## Stage 2: context ingestion

Before you read the review, open the pull request's **Files changed** tab and read the two files under `.gitar/`. Then read Gitar's finding, the comment the rule posted, and the **Rules** section of Gitar's dashboard comment.

The two files do different jobs. An instruction in `.gitar/review/` changes what the review looks for. A rule in `.gitar/rules/` makes Gitar take an action when a pull request event matches. This stage is review only, so don't fix or merge it.

## Stage 3: CI failure, then auto-apply and auto-merge

The pull request's `test` check fails. Read Gitar's CI analysis in its dashboard comment first, because applying the fix replaces it. Then post one comment.

If you set up merge controls, comment both commands, one per line. Done means the pull request is merged.

```text
gitar auto-apply:on
gitar auto-merge:on
```

If you skipped merge controls, comment only `gitar auto-apply:on`. Done means a Gitar commit and green CI.

Either way, check that Gitar's commit changed application code, not a test. Gitar approves the code, and GitHub won't merge until `test` is green, so it never merges on red.

## Troubleshooting

| Problem | What to do |
|---|---|
| No review after 5 minutes | Comment `gitar review` |
| Pull request opened against `sonar-samples` | Close it and use the link from setup step 4 |
| No `test` check on a pull request | Enable Actions (setup step 2), then close and reopen the pull request |
| Stage 3 shows no CI analysis | Comment `gitar review` |
| Gitar's dashboard says auto-merge wasn't armed | Check the three merge controls |

## Take it further

- **Reset and re-run.** Stage 3 merged into your `main`. Delete your fork (**Settings > Danger Zone**) and fork again with "Copy the `main` branch only" unchecked.
- **Make the Stage 2 context permanent.** Copy the `.gitar/` folder from the `stage-2` branch to `main` in your fork. The instruction and rule then apply to every pull request. Then write a rule of your own.
- **Reuse your coding agent's instructions.** Gitar reads `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, and files one level deep in `.cursor/rules/` and `.claude/rules/`. Add an `AGENTS.md` with one team rule, open a pull request, and watch the review apply it. Keep instruction files short, because Gitar's instruction budget is 8k tokens.
- **Write a skill.** Add `.gitar/skills/<name>/SKILL.md` with `name` and `description` frontmatter, then trigger it in plain language: `gitar run the <name> skill on this`. Slash syntax does nothing. Gitar also reads skills from `.claude/skills/`, `.agents/skills/`, and `.github/skills/`.
- **Set approval and merge criteria.** Write plain-language criteria in `.gitar/config/approve.md` and `.gitar/config/merge.md`. Gitar reads `merge.md` from the default branch only, so a pull request can't grant itself auto-merge.
- **Connect an integration (Pro).** Connect Slack or Jira under **Settings > Integrations**, then name it in a rule, for example "post a summary to #releases."
- **Useful commands.** `gitar review`, `gitar display:verbose`, and `gitar auto-apply:off`.
- **What Enterprise adds.** Knowledge with citations, cross-repo and cross-PR analysis, functional validation against linked issues, and Thorough review depth.
