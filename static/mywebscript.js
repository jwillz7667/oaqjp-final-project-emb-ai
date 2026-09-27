"use strict";

async function RunSentimentAnalysis() {
    const input = document.getElementById("textToAnalyze");
    const output = document.getElementById("system_response");
    const button = document.getElementById("analyzeButton");
    button.disabled = true;
    output.textContent = "Analyzing…";
    try {
        const query = new URLSearchParams({ textToAnalyze: input.value });
        const response = await fetch(`emotionDetector?${query}`, {
            signal: AbortSignal.timeout(40000),
            cache: "no-store"
        });
        output.textContent = await response.text();
    } catch {
        output.textContent = "Unable to reach the service. Please try again.";
    } finally {
        button.disabled = false;
    }
}
