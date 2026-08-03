# Game Glitch Investigator: Model Card and Responsible-AI Reflection

## System Overview and Current Status

Game Glitch Investigator is being extended into a retrieval-augmented investigation assistant. The intended system will accept a game name, platform, glitch description, when the glitch occurs, whether mods are installed, and troubleshooting already attempted. It will validate those fields, retrieve relevant local reports, and provide the retrieved evidence to an AI component that generates likely causes and troubleshooting steps.

The current repository contains the local knowledge base, keyword retriever, labeled reliability cases, and architecture design. The AI-generation component and investigation form are not integrated yet. This distinction is important: the retrieval test results described below demonstrate the reliability of the current retriever, not the accuracy or safety of a completed generative AI system.

All current knowledge-base entries are labeled as instructor-created synthetic demonstration records. They are not official bug reports and should not be presented as verified facts about a real game.

## Intended Use

The intended user is a player who wants an organized starting point for investigating a game glitch. The completed system should help the user compare symptoms with locally stored reports, understand which evidence influenced the investigation, and try low-risk troubleshooting steps in a sensible order.

The system should be treated as an investigation aid, not an authoritative diagnosis. Its output should use cautious language such as “possible cause” and should clearly say when the local knowledge base contains no relevant report.

## Limitations and Biases

### Small and synthetic knowledge base

The current knowledge base contains only three reports for a fictional `Example Game` on PC. This creates strong coverage bias: graphics, save-state, and mod-conflict symptoms are represented, while consoles, mobile platforms, networking failures, audio problems, accessibility issues, hardware faults, and many other categories are absent. Passing the current tests means the retriever works on these labeled examples; it does not prove that it generalizes to real games or unfamiliar descriptions.

### Keyword-matching limitations

The retriever compares normalized words rather than meanings. It may miss a relevant report when a user uses synonyms that do not occur in the report. For example, “rendering corruption” might not match a record written only with “visual artifacts.” It can also return weaker secondary matches when reports share common technical words such as “save,” “load,” or “disabled.”

Exact game and platform matches improve ranking, but metadata cannot create a result without meaningful description overlap. This reduces false matches but can also exclude a genuinely relevant cross-platform report.

### Source and labeling bias

The categories, symptom wording, possible causes, and recommendations reflect choices made by the people who created the synthetic records. Those choices determine which problems the system can recognize and which troubleshooting steps it favors. If future records disproportionately represent popular PC games or one type of player, retrieval quality will be worse for less-represented platforms, games, languages, and user communities.

### Generative-model limitations

Once generation is integrated, the model may overstate a weak match, combine details from different reports, invent an unsupported cause, or omit uncertainty. Retrieved context reduces hallucination risk but does not eliminate it. The generated category could also disagree with the category of the top retrieved report.

The current evaluation measures report ID and category retrieval, not factual accuracy, completeness, clarity, harmful instructions, or faithfulness of generated output. Those properties will require additional automated checks and human review after generation is implemented.

### Software limitations

The Streamlit application still runs the original number-guessing game and is not connected to `retrieve_glitches()`. Runtime investigation logging and full input validation are planned but not implemented. The complete test suite also contains three inherited failures because `logic_utils.py` still has refactoring placeholders.

## Potential Misuse and Prevention

### Presenting synthetic reports as official information

A user could copy an investigation and claim that it documents an official or confirmed game bug. To reduce this risk, every demonstration report includes an explicit synthetic source label. The UI and generated response should display that label and avoid terms such as “official,” “verified,” or “confirmed” unless a future record includes a real, checked citation.

### Unsafe or destructive troubleshooting

Generated advice could tell a user to delete save data, remove files, edit system configuration, download untrusted software, or disable security controls. Prevention should include output rules that prioritize reversible steps, require a backup before modifying saves or configuration, and reject instructions involving unknown downloads, credential sharing, anti-cheat circumvention, piracy, or security bypasses. Destructive actions should never be performed automatically.

### Cheating or bypassing game protections

Someone could frame a request as glitch troubleshooting while seeking help to exploit multiplayer bugs, evade anti-cheat tools, duplicate items, or gain an unfair advantage. The system should restrict its purpose to diagnosis, recovery, compatibility, and safe troubleshooting. Requests to weaponize a glitch or bypass protections should receive a refusal and, where appropriate, a suggestion to report the issue responsibly to the game developer.

### Privacy and log misuse

Free-text reports could contain usernames, account identifiers, file paths, server addresses, or API credentials. Logs should minimize stored content, avoid credentials and secrets, use sanitized error messages, and record only fields needed for reliability analysis. Generated JSON logs are excluded from Git so personal reports are not committed accidentally. Users should be told not to enter passwords, license keys, or other sensitive information.

### Overreliance on a plausible answer

A polished investigation might lead a user to treat an uncertain category as fact. The completed output should separate retrieved evidence, likely explanation, suggested troubleshooting, and uncertainty. It should show retrieved report IDs and explicitly state when there is no relevant report rather than asking the model to fill the evidence gap.

## Safeguards and Responsible Design Requirements

The completed system should enforce the following safeguards:

1. Validate required fields, types, and reasonable length limits before retrieval.
2. Treat the user's report as untrusted data, not as instructions that can override the system prompt.
3. Require meaningful symptom overlap before declaring a retrieved match.
4. Include report IDs and source labels in the investigation.
5. Keep retrieved evidence separate from model inference.
6. State uncertainty and provide a clear no-match response.
7. Recommend backups and reversible troubleshooting before risky changes.
8. Avoid secret values and unnecessary personal data in logs.
9. Return safe user-facing errors without exposing stack traces or credentials.
10. Use deterministic tests plus human review before describing the full system as reliable.

## Reliability Testing and What Was Surprising

The structured cases in `tests/test_cases.json` define an expected report ID and category for each synthetic query. `tests/test_retrieval.py` loads those cases and verifies that the expected report is ranked first. A separate test checks that an unrelated controller-battery description returns no reports.

Current retrieval result:

```text
2 tests passed
3 of 3 labeled cases returned the expected top report and category
1 of 1 unrelated cases correctly returned no report
```

The most surprising result was that the first scoring design could return reports for an unrelated description simply because the game and platform matched. That behavior looked reasonable at first because metadata should influence relevance, but it prevented the system from honestly reporting “no relevant report found.” The scorer was changed so game and platform improve ranking only after at least one meaningful description term matches.

Testing also showed that the correct report can be followed by a weaker secondary result. For the missing-progress example, the save-state report scores highest, but a mod-conflict report is also returned because both contain save/load vocabulary. This demonstrated that top-k retrieval is not equivalent to top-k truth: the AI must not treat every returned report as equally strong evidence.

These results are encouraging for the tiny demonstration set but should not be reported as general accuracy. A larger evaluation should include paraphrases, misspellings, different platforms, ambiguous symptoms, adversarial input, multiple simultaneous glitches, and cases with no supported category.

## Collaboration With AI

AI was used as a coding and planning collaborator during the project. I used it to inspect the repository, compare the assignment requirements with the existing files, propose a small retrieval architecture, implement the initial foundation, create tests, and improve documentation. I verified its work by reviewing the changed files, running retrieval calls against the labeled JSON cases, compiling the Python files, running pytest, and checking Git status before each commit.

### Helpful AI suggestion

A helpful suggestion was to begin with deterministic keyword retrieval instead of immediately adding embeddings or a vector database. That choice kept the first version understandable, offline, inexpensive, and easy to test. I verified the suggestion by running the labeled evaluation: every current case returned its expected top report and category, and the no-match test passed.

The AI also identified a meaningful flaw during verification: metadata bonuses alone could produce a match even when the symptoms were unrelated. Adding the no-match test reproduced the risk, and requiring description overlap corrected it.

### Flawed or incorrect AI suggestion

An earlier AI plan referred to giving retrieved reports to the “existing AI investigation logic.” That suggestion was based on an incorrect assumption. Repository inspection showed that `app.py` contains a Streamlit number-guessing game and that `logic_utils.py` contains unimplemented refactoring placeholders; there was no AI investigation service to connect.

The plan was corrected by keeping the first commit limited to the RAG foundation and documenting generation as a future integration milestone. This experience showed why AI recommendations must be checked against source code and test results rather than accepted because they sound consistent with the project description.

## Human Oversight

Human review remains necessary when adding or changing knowledge-base records, especially if a record is presented as real rather than synthetic. A reviewer should confirm the source, wording, category, and safety of recommended steps. Human evaluation will also be needed for generated investigations to check whether they are grounded, understandable, appropriately uncertain, non-destructive, and useful to a player.

Before deployment, human reviewers should evaluate a parseable set of representative outputs and record the input, retrieved report IDs, evaluation criteria, result, and reviewer notes. Failures should become regression cases when they can be tested automatically.

## Future Evaluation Priorities

- Measure top-1 category accuracy and top-k report recall on a larger labeled dataset.
- Evaluate no-match precision so unsupported requests do not receive fabricated evidence.
- Add tests for blank, oversized, malformed, and prompt-injection-style input.
- Compare keyword retrieval with semantic retrieval using the same evaluation cases.
- Check that generated claims can be traced to retrieved report fields.
- Record latency, retrieval scores, generated category, sanitized errors, and report IDs.
- Conduct structured human review of safety, clarity, grounding, and uncertainty.
- Test whether performance differs across platforms, writing styles, and represented game communities.
