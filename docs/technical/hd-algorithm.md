# Health data algorithm

It's designed to detect the problems of a person using its HealthData (object with all the responses to the user's questions).

## Original files

The algorithm is based on <a href="https://teams.microsoft.com/l/file/E8823988-B6E2-49ED-B60C-5E1403D74485?tenantId=5aab2be8-8083-494d-b86b-11091ccb0289&fileType=xlsx&objectUrl=https%3A%2F%2Fingage437.sharepoint.com%2Fsites%2FExperimentations%2FShared%20Documents%2FAI%20and%20ML%2FChatbots%2FFull%20Power%20app%2FPleine%20puissance%20-%20Arbre%20de%20d%C3%A9cision.xlsx&baseUrl=https%3A%2F%2Fingage437.sharepoint.com%2Fsites%2FExperimentations&serviceName=teams&threadId=19:a615c16473a8459aad220d8ffc82e895@thread.tacv2&groupId=7d12e89d-2bb1-4bfe-ad0c-76e9eff55c94" class="external-link" target="_blank">Stephane's excel</a>.

### Questions excel file

In the backend, the questions results are stored with a integer from 0 to 4. The questions themselves are stored in the <a href="https://teams.microsoft.com/l/file/E70D911C-F682-4668-B7CA-A7A21DBC5FCC?tenantId=5aab2be8-8083-494d-b86b-11091ccb0289&fileType=xlsx&objectUrl=https%3A%2F%2Fingage437.sharepoint.com%2Fsites%2FExperimentations%2FShared%20Documents%2FAI%20and%20ML%2FChatbots%2FFull%20Power%20app%2Fquestions.xlsx&baseUrl=https%3A%2F%2Fingage437.sharepoint.com%2Fsites%2FExperimentations&serviceName=teams&threadId=19:a615c16473a8459aad220d8ffc82e895@thread.tacv2&groupId=7d12e89d-2bb1-4bfe-ad0c-76e9eff55c94" class="external-link" target="_blank">questions excel</a> in teams.

It has 3 columns and multiple rows. The columns are:

- **variable:** it's the question's id. It's kind of related to the variable the user must respond. They are specified inside the coefficients file (link below, in the [internal links](#internal-links) section), as keys.
- **lang:** language of the question. Must be as an abbreviation.
- **question:** question itself. It's the actual question the chatbot will ask the user. A break line in the question or the character `~` can be used to split the chatbot's message into different messages, so the interface will render them as different messages.

The [update-questions script](../scripts/update-questions.md) is used to update the real chatbot's questions using the questions excel file. It checks the excel first. For example, for each `variable` (or question id) there must be 3 rows, one for each language supported (right now we support *spanish*, *french* and *english*). If this isn't true, the script will complain about the error and the exit, without updating the real questions.

## Internal links

- The algorithm is implemented in <a href="https://github.com/BelinguoAG/full-power-backend/blob/master/app/core/health_data.py" class="external-link" target="_blank">core/health_data.py</a>
- Coefficients are stored in <a href="https://github.com/BelinguoAG/full-power-backend/blob/master/app/db/files/coefficients.json" class="external-link" target="_blank">db/files/coefficients.json</a>

## Algorithm description

For each problem:

$p = \dfrac{\displaystyle\sum_{i=1}^n (5-R_i) \cdot C_i}{\displaystyle\sum_{i=1}^n 4C_i}$

- $n$: number of questions.
- $R_i$: different responses from the user (integer from 0 to 4).
- $C_i$: coefficients for each response.

Then, $p$ is compared to the setting `problem_ratio_threshold` (see [HealthData parsing in settings](../settings.md#healthdata-parsing)):

- If $p\geq problem \; ratio\; threshold$, the problem is real and the user is notified.
- If $p< problem \; ratio\; threshold$, the problem is not real and the user is **not** notified.
