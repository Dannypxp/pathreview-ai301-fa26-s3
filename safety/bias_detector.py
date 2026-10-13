"""Bias detection in generated feedback."""

import re

import structlog

logger = structlog.get_logger()


class BiasDetector:
    """Detect biased language in feedback."""

    # Genuinely dismissive phrases about educational background
    DISMISSIVE_PATTERNS = [
        r"(?:bootcamp|self-taught|online\s+course)\s+(?:education|training)\s+(?:is|are)\s+(?:insufficient|inadequate|lacks)",
        r"(?:coding\s+)?(?:bootcamp|self-taught|online\s+course)\s+(?:education|training|graduates?|developers?|programmers?|engineers?)\s+(?:lacks?|(?:is|are)\s+(?:lacking|missing))\s+(?:the\s+)?(?:rigor|fundamentals|proper\s+training)",
        r"(?:coding\s+)?(?:bootcamp|self-taught|online\s+course)\s+(?:graduates?|developers?|programmers?|engineers?)\s+(?:can't|cannot|can\s+not|won't|will\s+not)\b",
        r"(?:bootcamp|coding\s+bootcamp)\s+(?:doesn't|does\s+not)\s+prepare\s+(?:you|developers?)",
        r"(?:self-taught|bootcamp)\s+(?:graduates?\s+|developers?\s+|programmers?\s+|engineers?\s+)?(?:is|are)\s+(?:not|never)\s+(?:equal|comparable)\s+to\s+(?:university|traditional|formal)",
        r"(?:bootcamp|self-taught|online\s+course)\s+(?:attendance|education|training|background)\s+(?:means|implies|proves|indicates)\s+(?:inadequate|insufficient|poor|no|a\s+lack)",
        r"\blacks?\s+the\s+(?:rigor|fundamentals)\s+of\s+(?:a\s+)?(?:formal|traditional|university)",
    ]

    # Demographic assumptions (about age, background, identity)
    DEMOGRAPHIC_PATTERNS = [
        r"(?:(?:young|old|aged)\s+)+(?:persons?|people|developers?|programmers?|engineers?)\s+(?:can't|cannot|can\s+not|won't|will\s+not)",
        r"(?:person\s+from|coming\s+from)\s+(?:poor|rich|working[\s-]?class)",
        r"(?:persons?|people|developers?|programmers?|engineers?)\s+(?:from|coming\s+from)\s+(?:a\s+)?(?:poor|rich|working[\s-]?class)\b.*?(?:can't|cannot|won't|struggle)",
        r"(?:immigrant|international|foreign)\s+(?:developers?|programmers?|engineers?).*?(?:can't|cannot|won't|struggle|lacks?)",
    ]

    @staticmethod
    def detect_bias(text: str) -> tuple[bool, str]:
        """Detect biased language in feedback.

        Args:
            text: Feedback text

        Returns:
            Tuple of (is_biased, reason)
        """
        # Check for dismissive language about education
        for pattern in BiasDetector.DISMISSIVE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                reason = "Dismissive language about educational background"
                logger.warning("bias_detected", reason=reason)
                return True, reason

        # Check for demographic assumptions
        for pattern in BiasDetector.DEMOGRAPHIC_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                reason = "Demographic assumptions detected"
                logger.warning("bias_detected", reason=reason)
                return True, reason

        return False, ""
