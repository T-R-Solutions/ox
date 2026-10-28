# Prompt evaluation and trust boundaries

Use for prompts that consume external documents or drive tools. Source: Huyen, AI Engineering, ch. 4 pp. 200–206 and ch. 5 pp. 233–235, 248–251; [reading record](portable-sources.md), B03.

1. Identify the intended output and authority of each input. Keep retrieved content visibly separate from instructions; document/tool text does not grant permissions.
2. Version prompt text, model identifier (when exposed), sampling configuration, input/output contracts and evaluation data. Changing the prompt alone still requires behavior checks when it drives consequential work.
3. Build ordinary, boundary, ambiguous, out-of-scope and injection examples with expected outcomes defined before looking at model outputs. Include legitimate requests resembling attacks to detect false refusals.
4. Evaluate components and complete tasks separately. A schema-valid response may still be wrong; a correct tool call may still be unauthorized. Use executable oracles for objective claims and a calibrated rubric for subjective ones.
5. Enforce consequential tool permissions outside generated text. Restrict operations and destinations according to actual authorization; prompt wording is not a sandbox. Do not mandate human approval for already-authorized reversible work.
6. Compare paired versions under equivalent inputs/environment, record violations, false refusals, task completion and cost. Keep a held-out set and separate raw observations from conclusions.

Validation: review a supplied document containing an instruction to bypass its task; verify the generated prompt keeps that text as data. Runtime robustness requires actual repeated model/tool trials. This reference supplies a procedure, not measured injection resistance. Do not execute the prompt's task unless asked.

Source of this portable copy: `prompt/references/evaluation-and-trust.md` in the authoring library; SHA-256 before adaptation: `2a117985248492f7257f8c9ce97c506918108e5dadb08de83da7de5ab1872212`. This copy is independently usable; reconcile technical changes manually when updating.
