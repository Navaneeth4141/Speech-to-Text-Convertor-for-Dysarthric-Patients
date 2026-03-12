/**
 * Metrics Display Module
 * Handles WER/CER visualization and improvement tracking
 */

class MetricsDisplay {
    constructor() {
        this.werValue = document.getElementById('werValue');
        this.cerValue = document.getElementById('cerValue');
        this.werCircle = document.querySelector('.wer-progress');
        this.cerCircle = document.querySelector('.cer-progress');
        this.improvementValue = document.getElementById('improvementValue');
        this.improvementBadge = document.getElementById('improvementBadge');

        // Circle circumference for animation
        this.circumference = 2 * Math.PI * 45; // radius = 45
    }

    updateMetrics(metrics) {
        if (!metrics) return;

        // Animate WER
        this.animateMetric(
            this.werValue,
            this.werCircle,
            metrics.wer,
            true // lower is better
        );

        // Animate CER
        this.animateMetric(
            this.cerValue,
            this.cerCircle,
            metrics.cer,
            true // lower is better
        );

        // Update improvement
        if (this.improvementValue && metrics.improvement) {
            this.animateNumber(this.improvementValue, metrics.improvement, '%');
        }
    }

    animateMetric(valueElement, progressElement, targetValue, lowerIsBetter = true) {
        if (!valueElement) return;

        // Animate the number
        this.animateNumber(valueElement, targetValue, '%');

        // Animate the circle progress
        if (progressElement) {
            // For error rates, we want to show how much is "good" (100 - error)
            const progressPercent = lowerIsBetter ? (100 - targetValue) : targetValue;
            const offset = this.circumference - (progressPercent / 100) * this.circumference;

            progressElement.style.strokeDasharray = this.circumference;
            progressElement.style.strokeDashoffset = this.circumference;

            // Trigger animation
            setTimeout(() => {
                progressElement.style.transition = 'stroke-dashoffset 1s ease-out';
                progressElement.style.strokeDashoffset = offset;
            }, 100);
        }
    }

    animateNumber(element, targetValue, suffix = '') {
        if (!element) return;

        const startValue = 0;
        const duration = 1000;
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function
            const easeOutQuad = 1 - (1 - progress) * (1 - progress);

            const currentValue = startValue + (targetValue - startValue) * easeOutQuad;
            element.textContent = currentValue.toFixed(1) + suffix;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    reset() {
        if (this.werValue) this.werValue.textContent = '--%';
        if (this.cerValue) this.cerValue.textContent = '--%';
        if (this.improvementValue) this.improvementValue.textContent = '--';

        // Reset circle progress
        if (this.werCircle) {
            this.werCircle.style.strokeDashoffset = this.circumference;
        }
        if (this.cerCircle) {
            this.cerCircle.style.strokeDashoffset = this.circumference;
        }
    }

    /**
     * Calculate and display comparison metrics between two transcriptions
     */
    compareTranscriptions(reference, baseline, optimized) {
        const baselineMetrics = this.calculateErrors(reference, baseline);
        const optimizedMetrics = this.calculateErrors(reference, optimized);

        const werImprovement = ((baselineMetrics.wer - optimizedMetrics.wer) / baselineMetrics.wer) * 100;
        const cerImprovement = ((baselineMetrics.cer - optimizedMetrics.cer) / baselineMetrics.cer) * 100;

        return {
            baseline: baselineMetrics,
            optimized: optimizedMetrics,
            werImprovement: werImprovement,
            cerImprovement: cerImprovement,
            averageImprovement: (werImprovement + cerImprovement) / 2
        };
    }

    calculateErrors(reference, hypothesis) {
        // Word Error Rate
        const refWords = reference.toLowerCase().split(/\s+/);
        const hypWords = hypothesis.toLowerCase().split(/\s+/);
        const wordErrors = this.levenshteinDistance(refWords, hypWords);
        const wer = (wordErrors / refWords.length) * 100;

        // Character Error Rate
        const refChars = reference.toLowerCase().replace(/\s/g, '').split('');
        const hypChars = hypothesis.toLowerCase().replace(/\s/g, '').split('');
        const charErrors = this.levenshteinDistance(refChars, hypChars);
        const cer = (charErrors / refChars.length) * 100;

        return { wer, cer };
    }

    levenshteinDistance(arr1, arr2) {
        const m = arr1.length;
        const n = arr2.length;
        const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

        for (let i = 0; i <= m; i++) dp[i][0] = i;
        for (let j = 0; j <= n; j++) dp[0][j] = j;

        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (arr1[i - 1] === arr2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(
                        dp[i - 1][j],
                        dp[i][j - 1],
                        dp[i - 1][j - 1]
                    );
                }
            }
        }

        return dp[m][n];
    }
}

// Initialize if on app page
if (document.getElementById('werValue')) {
    window.metricsDisplay = new MetricsDisplay();
}
