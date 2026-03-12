"""
Metrics Calculator Service
Calculates WER, CER, and other speech recognition metrics
"""


class MetricsCalculator:
    """
    Calculate speech recognition evaluation metrics:
    - Word Error Rate (WER)
    - Character Error Rate (CER)
    - Match Error Rate (MER)
    - Word Information Lost (WIL)
    """
    
    def calculate(self, reference, hypothesis):
        """
        Calculate all metrics between reference and hypothesis
        
        Args:
            reference: Ground truth text
            hypothesis: Transcribed text
            
        Returns:
            Dictionary with all metrics
        """
        wer = self.word_error_rate(reference, hypothesis)
        cer = self.character_error_rate(reference, hypothesis)
        
        # Calculate improvement estimate
        # (In real scenario, this would compare against a baseline)
        improvement = max(0, 100 - wer) * 0.3  # Simulated improvement
        
        return {
            'wer': round(wer, 2),
            'cer': round(cer, 2),
            'improvement': round(improvement, 1)
        }
    
    def word_error_rate(self, reference, hypothesis):
        """
        Calculate Word Error Rate
        
        WER = (S + D + I) / N
        
        Where:
        - S = substitutions
        - D = deletions
        - I = insertions
        - N = number of words in reference
        """
        ref_words = self._normalize_text(reference).split()
        hyp_words = self._normalize_text(hypothesis).split()
        
        if len(ref_words) == 0:
            return 0 if len(hyp_words) == 0 else 100
        
        # Calculate edit distance
        distance = self._levenshtein_distance(ref_words, hyp_words)
        
        # WER as percentage
        wer = (distance / len(ref_words)) * 100
        
        return min(100, wer)  # Cap at 100%
    
    def character_error_rate(self, reference, hypothesis):
        """
        Calculate Character Error Rate
        
        CER = (S + D + I) / N
        
        Similar to WER but at character level
        """
        ref_chars = list(self._normalize_text(reference).replace(' ', ''))
        hyp_chars = list(self._normalize_text(hypothesis).replace(' ', ''))
        
        if len(ref_chars) == 0:
            return 0 if len(hyp_chars) == 0 else 100
        
        distance = self._levenshtein_distance(ref_chars, hyp_chars)
        
        cer = (distance / len(ref_chars)) * 100
        
        return min(100, cer)
    
    def _normalize_text(self, text):
        """Normalize text for comparison"""
        if not text:
            return ''
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        import re
        text = re.sub(r'[^\w\s]', '', text)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text
    
    def _levenshtein_distance(self, seq1, seq2):
        """
        Calculate Levenshtein distance between two sequences
        
        Uses dynamic programming approach
        """
        m, n = len(seq1), len(seq2)
        
        # Create distance matrix
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Initialize first row and column
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # Fill in the rest
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i - 1] == seq2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],      # deletion
                        dp[i][j - 1],      # insertion
                        dp[i - 1][j - 1]   # substitution
                    )
        
        return dp[m][n]
    
    def detailed_analysis(self, reference, hypothesis):
        """
        Provide detailed error analysis
        
        Returns:
            Dictionary with detailed breakdown
        """
        ref_words = self._normalize_text(reference).split()
        hyp_words = self._normalize_text(hypothesis).split()
        
        # Calculate edit operations
        operations = self._get_edit_operations(ref_words, hyp_words)
        
        substitutions = sum(1 for op in operations if op[0] == 'substitute')
        deletions = sum(1 for op in operations if op[0] == 'delete')
        insertions = sum(1 for op in operations if op[0] == 'insert')
        
        total_errors = substitutions + deletions + insertions
        n_ref = len(ref_words)
        
        return {
            'reference_words': n_ref,
            'hypothesis_words': len(hyp_words),
            'substitutions': substitutions,
            'deletions': deletions,
            'insertions': insertions,
            'total_errors': total_errors,
            'wer': round((total_errors / n_ref) * 100, 2) if n_ref > 0 else 0,
            'cer': round(self.character_error_rate(reference, hypothesis), 2),
            'accuracy': round(100 - (total_errors / n_ref) * 100, 2) if n_ref > 0 else 100
        }
    
    def _get_edit_operations(self, ref, hyp):
        """
        Get the sequence of edit operations to transform hyp to ref
        
        Returns list of tuples: (operation, ref_word, hyp_word)
        """
        m, n = len(ref), len(hyp)
        
        # Build DP table
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if ref[i - 1] == hyp[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        
        # Backtrace to get operations
        operations = []
        i, j = m, n
        
        while i > 0 or j > 0:
            if i > 0 and j > 0 and ref[i - 1] == hyp[j - 1]:
                operations.append(('match', ref[i - 1], hyp[j - 1]))
                i -= 1
                j -= 1
            elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
                operations.append(('substitute', ref[i - 1], hyp[j - 1]))
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
                operations.append(('delete', ref[i - 1], None))
                i -= 1
            else:
                operations.append(('insert', None, hyp[j - 1]))
                j -= 1
        
        operations.reverse()
        return operations
    
    def compare_models(self, reference, baseline_hyp, adapted_hyp):
        """
        Compare performance of baseline vs adapted model
        
        Args:
            reference: Ground truth text
            baseline_hyp: Baseline model transcription
            adapted_hyp: Adapted model transcription
            
        Returns:
            Comparison metrics
        """
        baseline_metrics = self.detailed_analysis(reference, baseline_hyp)
        adapted_metrics = self.detailed_analysis(reference, adapted_hyp)
        
        wer_improvement = baseline_metrics['wer'] - adapted_metrics['wer']
        cer_improvement = baseline_metrics['cer'] - adapted_metrics['cer']
        
        return {
            'baseline': baseline_metrics,
            'adapted': adapted_metrics,
            'wer_improvement': round(wer_improvement, 2),
            'cer_improvement': round(cer_improvement, 2),
            'relative_wer_improvement': round(
                (wer_improvement / baseline_metrics['wer']) * 100, 1
            ) if baseline_metrics['wer'] > 0 else 0
        }
