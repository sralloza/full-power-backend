# Health data algorithm

It's designed to detect the problems of a person using its HealthData (object with all the responses to the user's questions).

## Original files

### Questions excel file

It has 3 columns and multiple rows. The columns are:

- **variable:** it's the question's id. It's kind of related to the variable the user must respond. They are specified inside the coefficients file (link below, in the [internal links](#internal-links) section), as keys.
- **lang:** language of the question. Must be as an abbreviation.
- **question:** question itself. It's the actual question the chatbot will ask the user. A break line in the question or the character `~` can be used to split the chatbot's message into different messages, so the interface will render them as different messages.

The [update-questions script](../scripts/update-questions.md) is used to update the real chatbot's questions using the questions excel file. It checks the excel first. For example, for each `variable` (or question id) there must be 3 rows, one for each language supported (right now we support *spanish*, *french* and *english*). If this isn't true, the script will complain about the error and the exit, without updating the real questions.

## Internal links

- The algorithm is implemented in <a href="https://github.com/sralloza/full-power-backend/blob/master/app/core/health_data.py" class="external-link" target="_blank">core/health_data.py</a>
- Coefficients are stored in <a href="https://github.com/sralloza/full-power-backend/blob/master/app/db/files/coefficients.json" class="external-link" target="_blank">db/files/coefficients.json</a>

## Algorithm description

For each problem:

$p = \dfrac{\displaystyle\sum_{i=1}^n (5-R_i) \cdot C_i}{\displaystyle\sum_{i=1}^n 4C_i}$

- $n$: number of questions.
- $R_i$: different responses from the user (integer from 0 to 4).
- $C_i$: coefficients for each response.

Finally, $p$ is analysed to check if it is really a problem:

- Values below 0.33 means it's not a real problem.
- Values between 0.33 and 0.66 means it's a **light** problem.
- Values above 0.66 indicate that the problem is a **serious** problem.

Finally, the user is notified with a description of all the problems.
