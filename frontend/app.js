(function () {
  const apiBaseUrl = (
    window.WORDLE_SOLVER_CONFIG &&
    window.WORDLE_SOLVER_CONFIG.apiBaseUrl
  ) || "";
  const backendConfigured = Boolean(String(apiBaseUrl).trim());

  const state = {
    rows: [createEmptyRow()],
    loading: false,
    result: null,
  };

  const boardElement = document.getElementById("board");
  const addRowButton = document.getElementById("add-row-button");
  const removeRowButton = document.getElementById("remove-row-button");
  const solveButton = document.getElementById("solve-button");
  const statusMessageElement = document.getElementById("status-message");
  const backendNoticeElement = document.getElementById("backend-notice");
  const resultsPanel = document.getElementById("results-panel");
  const bestGuessTiles = document.getElementById("best-guess-tiles");
  const rankedList = document.getElementById("ranked-list");
  const remainingCount = document.getElementById("remaining-count");
  const rankingLabel = document.getElementById("ranking-label");
  const strategyLine = document.getElementById("strategy-line");
  const candidatesCard = document.getElementById("candidates-card");
  const candidateList = document.getElementById("candidate-list");

  const feedbackClassByValue = {
    0: "is-absent",
    1: "is-present",
    2: "is-correct",
  };

  const feedbackLabelByValue = {
    0: "Absent",
    1: "Present",
    2: "Correct",
  };

  function createEmptyRow() {
    return {
      letters: ["", "", "", "", ""],
      feedback: [0, 0, 0, 0, 0],
    };
  }

  function renderBoard() {
    boardElement.innerHTML = state.rows
      .map((row, rowIndex) => {
        const letterTiles = row.letters
          .map((letter, columnIndex) => {
            const feedbackClass = feedbackClassByValue[row.feedback[columnIndex]];
            return `
              <input
                type="text"
                inputmode="text"
                autocomplete="off"
                maxlength="1"
                class="guess-input ${feedbackClass}"
                data-row-index="${rowIndex}"
                data-column-index="${columnIndex}"
                value="${escapeAttribute(letter.toUpperCase())}"
                aria-label="Row ${rowIndex + 1} letter ${columnIndex + 1}"
              />
            `;
          })
          .join("");

        const feedbackTiles = row.feedback
          .map((feedbackValue, columnIndex) => {
            const feedbackClass = feedbackClassByValue[feedbackValue];
            const feedbackLabel = feedbackLabelByValue[feedbackValue];
            return `
              <button
                type="button"
                class="feedback-button ${feedbackClass}"
                data-feedback-row-index="${rowIndex}"
                data-feedback-column-index="${columnIndex}"
                aria-label="Row ${rowIndex + 1} result ${columnIndex + 1}: ${feedbackLabel}"
                title="Click to cycle result"
              >
                ${feedbackValue}
              </button>
            `;
          })
          .join("");

        return `
          <section class="board-row">
            <div class="tile-row">${letterTiles}</div>
            <div class="feedback-row">${feedbackTiles}</div>
          </section>
        `;
      })
      .join("");

    removeRowButton.disabled = state.loading || state.rows.length === 1;
    addRowButton.disabled = state.loading;
    solveButton.disabled = state.loading || !backendConfigured;
  }

  function renderResults() {
    if (!state.result) {
      resultsPanel.hidden = true;
      return;
    }

    const result = state.result;
    resultsPanel.hidden = false;
    rankingLabel.textContent = result.ranking_label || "";
    strategyLine.textContent = formatStrategy(result.strategy);
    remainingCount.textContent = String(result.remaining_candidate_count);

    bestGuessTiles.innerHTML = buildWordTilesMarkup(result.best_guess);

    rankedList.innerHTML = (result.top_guesses || [])
      .map((guess) => {
        const scoreParts = [];
        if (guess.score !== undefined && guess.score !== null) {
          scoreParts.push(formatScore(guess.score));
        }
        if (guess.tie_breaker !== undefined && guess.tie_breaker !== null) {
          scoreParts.push(`tie ${formatScore(guess.tie_breaker)}`);
        }

        return `
          <li class="ranked-item">
            <span class="ranked-word">${escapeHtml(guess.word)}</span>
            <span class="ranked-score">${escapeHtml(scoreParts.join(" · "))}</span>
          </li>
        `;
      })
      .join("");

    if (result.remaining_candidates && result.remaining_candidates.length) {
      candidatesCard.hidden = false;
      candidateList.innerHTML = result.remaining_candidates
        .map((candidate) => `<span class="candidate-chip">${escapeHtml(candidate)}</span>`)
        .join("");
    } else {
      candidatesCard.hidden = true;
      candidateList.innerHTML = "";
    }
  }

  function buildWordTilesMarkup(word) {
    return String(word || "")
      .padEnd(5, " ")
      .slice(0, 5)
      .split("")
      .map((letter) => `<span class="word-tile is-correct">${escapeHtml(letter.trim())}</span>`)
      .join("");
  }

  function formatStrategy(strategy) {
    if (!strategy) {
      return "";
    }

    const map = {
      "precomputed-opening": "Using the precomputed opening-word ranking from the legacy solver.",
      "expected-remaining": "Using the stronger expected-remaining ranking on the narrowed answer set.",
      "frequency-heuristic": "Using the legacy letter-frequency heuristic on the remaining candidates.",
      "resolved-candidate": "Only one candidate remains.",
    };

    return map[strategy] || strategy;
  }

  function formatScore(score) {
    const numeric = Number(score);
    if (Number.isInteger(numeric)) {
      return numeric.toString();
    }
    return numeric.toFixed(2).replace(/\.00$/, "");
  }

  function setStatus(message, type) {
    statusMessageElement.textContent = message || "";
    statusMessageElement.classList.remove("is-error", "is-success");
    if (type === "error") {
      statusMessageElement.classList.add("is-error");
    }
    if (type === "success") {
      statusMessageElement.classList.add("is-success");
    }
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function escapeAttribute(value) {
    return escapeHtml(value);
  }

  function focusCell(rowIndex, columnIndex) {
    const selector = `[data-row-index="${rowIndex}"][data-column-index="${columnIndex}"]`;
    const target = boardElement.querySelector(selector);
    if (target) {
      target.focus();
      target.select();
    }
  }

  function fillLetters(rowIndex, startColumnIndex, text) {
    const letters = text.replace(/[^a-z]/gi, "").toLowerCase().slice(0, 5);
    if (!letters) {
      return;
    }

    let nextColumnIndex = startColumnIndex;
    for (const character of letters) {
      if (nextColumnIndex > 4) {
        break;
      }
      state.rows[rowIndex].letters[nextColumnIndex] = character;
      nextColumnIndex += 1;
    }

    renderBoard();
    focusCell(rowIndex, Math.min(nextColumnIndex, 4));
  }

  function buildPayload() {
    const guesses = [];

    state.rows.forEach((row, rowIndex) => {
      const word = row.letters.join("").trim();
      const hasAnyLetter = row.letters.some(Boolean);

      if (!hasAnyLetter) {
        return;
      }

      if (word.length !== 5) {
        throw new Error(`Row ${rowIndex + 1} needs a complete 5-letter guess.`);
      }

      guesses.push({
        word,
        feedback: row.feedback.join(""),
      });
    });

    return { guesses };
  }

  async function submitBoard() {
    if (!backendConfigured) {
      setStatus(
        "Backend not configured yet. Deploy the API and set the production API base URL to enable solving.",
        "error"
      );
      return;
    }

    let payload;
    try {
      payload = buildPayload();
    } catch (error) {
      setStatus(error.message, "error");
      return;
    }

    state.loading = true;
    renderBoard();
    setStatus("Running solver...", null);

    try {
      const response = await fetch(`${apiBaseUrl}/solve`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.error || "Solver request failed.");
      }

      state.result = result;
      renderResults();
      setStatus("Solver finished.", "success");
    } catch (error) {
      state.result = null;
      renderResults();
      setStatus(error.message || "Solver request failed.", "error");
    } finally {
      state.loading = false;
      renderBoard();
    }
  }

  boardElement.addEventListener("input", (event) => {
    const target = event.target;
    if (!target.matches(".guess-input")) {
      return;
    }

    const rowIndex = Number(target.dataset.rowIndex);
    const columnIndex = Number(target.dataset.columnIndex);
    const rawValue = target.value;

    if (rawValue.length > 1) {
      fillLetters(rowIndex, columnIndex, rawValue);
      return;
    }

    const letter = rawValue.replace(/[^a-z]/gi, "").toLowerCase();
    state.rows[rowIndex].letters[columnIndex] = letter;
    renderBoard();

    if (letter && columnIndex < 4) {
      focusCell(rowIndex, columnIndex + 1);
    } else {
      focusCell(rowIndex, columnIndex);
    }
  });

  boardElement.addEventListener("keydown", (event) => {
    const target = event.target;
    if (!target.matches(".guess-input")) {
      return;
    }

    const rowIndex = Number(target.dataset.rowIndex);
    const columnIndex = Number(target.dataset.columnIndex);

    if (event.key === "Backspace" && !state.rows[rowIndex].letters[columnIndex] && columnIndex > 0) {
      state.rows[rowIndex].letters[columnIndex - 1] = "";
      renderBoard();
      focusCell(rowIndex, columnIndex - 1);
      event.preventDefault();
      return;
    }

    if (event.key === "ArrowLeft" && columnIndex > 0) {
      focusCell(rowIndex, columnIndex - 1);
      event.preventDefault();
    }

    if (event.key === "ArrowRight" && columnIndex < 4) {
      focusCell(rowIndex, columnIndex + 1);
      event.preventDefault();
    }
  });

  boardElement.addEventListener("paste", (event) => {
    const target = event.target;
    if (!target.matches(".guess-input")) {
      return;
    }

    const pastedText = event.clipboardData.getData("text");
    if (!pastedText) {
      return;
    }

    const rowIndex = Number(target.dataset.rowIndex);
    const columnIndex = Number(target.dataset.columnIndex);
    fillLetters(rowIndex, columnIndex, pastedText);
    event.preventDefault();
  });

  boardElement.addEventListener("click", (event) => {
    const target = event.target;
    if (!target.matches(".feedback-button")) {
      return;
    }

    const rowIndex = Number(target.dataset.feedbackRowIndex);
    const columnIndex = Number(target.dataset.feedbackColumnIndex);
    const currentValue = state.rows[rowIndex].feedback[columnIndex];
    state.rows[rowIndex].feedback[columnIndex] = (currentValue + 1) % 3;
    renderBoard();
  });

  addRowButton.addEventListener("click", () => {
    state.rows.push(createEmptyRow());
    renderBoard();
    focusCell(state.rows.length - 1, 0);
  });

  removeRowButton.addEventListener("click", () => {
    if (state.rows.length === 1) {
      return;
    }
    state.rows.pop();
    renderBoard();
  });

  solveButton.addEventListener("click", submitBoard);

  if (!backendConfigured) {
    backendNoticeElement.hidden = false;
    backendNoticeElement.textContent =
      "Backend not configured yet. The board is live, but solve requests stay disabled until a real API base URL is added.";
    setStatus(
      "Submit is disabled until the production API base URL is configured.",
      null
    );
  }

  renderBoard();
  renderResults();
})();
