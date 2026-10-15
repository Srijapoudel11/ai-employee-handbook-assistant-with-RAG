
# Evaluation Results Summary

## Summary Overview

- **Date of Evaluation:** 2026-10-15
- **Model Evaluated:** `llama3.2` through Ollama
- **Total Test Cases Executed:** 5 manual test cases
- **Passed:** 5
- **Failed:** 0
- **Pass Rate:** 100%

Additionally, all 10 automated tests passed using `python -m pytest`.

## Performance by Category

| Category | Total Cases | Passed | Failed | Pass Rate |
|---|---:|---:|---:|---:|
| Successful Cases | 2 | 2 | 0 | 100% |
| Difficult Cases | 1 | 1 | 0 | 100% |
| Failure / Edge Cases | 2 | 2 | 0 | 100% |
| **Total** | **5** | **5** | **0** | **100%** |

## Key Findings & Failure Analysis

### What worked well

- The AI correctly answered annual leave questions using Section 3 of the handbook.
- The AI correctly explained the remote work policy using Section 5.
- The AI understood the alternative wording "holiday time" and retrieved the annual leave policy.
- The AI correctly refused to invent an answer about the cafeteria lunch menu.
- The application displayed a friendly message when the question was empty.
- The application displayed relevant handbook sources for successful questions.

### Observed failure modes

No failures occurred in the five recorded manual evaluation cases.

However, during an earlier test, the AI mentioned an unverified subsection, "3.2". This indicates that generated source references may sometimes be inaccurate.

The keyword-based RAG retrieval may also struggle with questions using unfamiliar wording. These limitations were not comprehensively tested.

## Action Items & Improvements

- [ ] Improve the accuracy of AI-generated source references.
- [ ] Evaluate more question variations to identify retrieval limitations.

These are identified future improvements, not completed features.

## Conclusion

The AI Employee Handbook Assistant successfully passed all five recorded manual test cases and all ten automated tests.

The results demonstrate that the integrated Gradio interface, Ollama model, and RAG retrieval system work for the tested handbook questions.

Further evaluation would be necessary to assess broader reliability.
