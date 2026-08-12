from __future__ import annotations

from dataclasses import dataclass

from models import DomainAssessment, RiskLevel, Task


@dataclass(frozen=True)
class DomainRule:
    name: str
    keywords: tuple[str, ...]
    risk_level: RiskLevel
    source_types: tuple[str, ...]
    standards: tuple[str, ...]
    criteria: tuple[str, ...]


class DomainResolver:
    """Deterministic Phase 3 baseline resolver for task domain and review needs."""

    RULES: tuple[DomainRule, ...] = (
        DomainRule(
            name="medicine",
            keywords=("medical", "medicine", "clinical", "diagnosis", "treatment", "patient", "медич", "діагноз", "лікуван", "пацієнт"),
            risk_level=RiskLevel.CRITICAL,
            source_types=("OFFICIAL", "PEER_REVIEWED", "PRIMARY_DOCUMENT", "GOVERNMENT"),
            standards=("current clinical guidelines and applicable official health guidance",),
            criteria=("clinical evidence quality", "patient-safety implications", "freshness of medical guidance", "claim-to-evidence consistency"),
        ),
        DomainRule(
            name="law",
            keywords=("legal", "law", "statute", "regulation", "court", "contract", "юрид", "закон", "право", "суд", "договір"),
            risk_level=RiskLevel.HIGH,
            source_types=("OFFICIAL", "PRIMARY_DOCUMENT", "GOVERNMENT"),
            standards=("applicable statutes, regulations, and official legal texts",),
            criteria=("jurisdiction correctness", "authority of legal sources", "current legal status", "distinction between law and interpretation"),
        ),
        DomainRule(
            name="finance",
            keywords=("finance", "financial", "investment", "trading", "stock", "crypto", "market", "фінанс", "інвест", "трейдинг", "торгів", "акці", "крипт"),
            risk_level=RiskLevel.HIGH,
            source_types=("OFFICIAL", "PRIMARY_DOCUMENT", "GOVERNMENT", "PROFESSIONAL_PUBLICATION"),
            standards=("applicable financial disclosures, regulations, and primary market data",),
            criteria=("data freshness", "source authority", "risk disclosure", "separation of fact, estimate, and recommendation"),
        ),
        DomainRule(
            name="construction",
            keywords=("construction", "structural", "concrete", "building", "load-bearing", "будів", "конструкц", "бетон", "несуч"),
            risk_level=RiskLevel.HIGH,
            source_types=("STANDARD", "OFFICIAL", "PRIMARY_DOCUMENT", "PROFESSIONAL_PUBLICATION"),
            standards=("applicable building codes and structural standards",),
            criteria=("technical correctness", "applicable standards", "safety implications", "assumptions and load conditions"),
        ),
        DomainRule(
            name="geodesy",
            keywords=("geodesy", "geodetic", "surveying", "gnss", "rtk", "coordinate", "deformation monitoring", "геодез", "координат", "нівелір", "зніман", "деформац"),
            risk_level=RiskLevel.HIGH,
            source_types=("STANDARD", "OFFICIAL", "PRIMARY_DOCUMENT", "MANUFACTURER", "ACADEMIC"),
            standards=("applicable geodetic standards and validated equipment specifications",),
            criteria=("measurement methodology", "accuracy and uncertainty", "reference-system correctness", "equipment and correction-source limitations"),
        ),
        DomainRule(
            name="software_engineering",
            keywords=("software", "python", "api", "database", "code", "programming", "architecture", "програм", "код", "база даних", "api", "архітектур"),
            risk_level=RiskLevel.MEDIUM,
            source_types=("OFFICIAL", "PRIMARY_DOCUMENT", "REFERENCE"),
            standards=("official documentation and applicable technical specifications",),
            criteria=("technical correctness", "interface compatibility", "failure handling", "maintainability and testability"),
        ),
        DomainRule(
            name="military",
            keywords=("military", "defense", "defence", "armed forces", "військ", "оборона", "збройн"),
            risk_level=RiskLevel.HIGH,
            source_types=("OFFICIAL", "PRIMARY_DOCUMENT", "GOVERNMENT", "ACADEMIC"),
            standards=("applicable official doctrine, regulations, and technical publications",),
            criteria=("source authority", "operational context", "terminology accuracy", "uncertainty and limitations"),
        ),
        DomainRule(
            name="literary_analysis",
            keywords=("literature", "literary", "novel", "poem", "author", "fiction", "літератур", "роман", "вірш", "автор", "худож"),
            risk_level=RiskLevel.LOW,
            source_types=("PRIMARY_DOCUMENT", "ACADEMIC", "REFERENCE"),
            standards=("primary text and relevant scholarly criticism",),
            criteria=("faithfulness to the primary text", "interpretive support", "contextual accuracy", "distinction between evidence and interpretation"),
        ),
    )

    GENERIC_TASK_TYPES = {"auto", "unspecified", "general", "research"}

    def resolve(self, task: Task) -> DomainAssessment:
        text = task.user_request.casefold()
        matched = [rule for rule in self.RULES if any(keyword.casefold() in text for keyword in rule.keywords)]

        if matched:
            primary = matched[0]
            secondary = [rule.name for rule in matched[1:]]
            risk = max((rule.risk_level for rule in matched), key=self._risk_rank)
            source_types = self._dedupe(item for rule in matched for item in rule.source_types)
            standards = self._dedupe(item for rule in matched for item in rule.standards)
            criteria = self._dedupe(item for rule in matched for item in rule.criteria)
            uncertainties: list[str] = []
        else:
            primary = DomainRule(
                name="general_research",
                keywords=(),
                risk_level=RiskLevel.MEDIUM,
                source_types=("OFFICIAL", "PRIMARY_DOCUMENT", "ACADEMIC", "REFERENCE"),
                standards=("task-relevant authoritative sources and primary evidence",),
                criteria=("factual correctness", "source quality", "claim support", "explicit uncertainty"),
            )
            secondary = []
            risk = primary.risk_level
            source_types = list(primary.source_types)
            standards = list(primary.standards)
            criteria = list(primary.criteria)
            uncertainties = ["Domain classification confidence is limited; user confirmation may be required."]

        return DomainAssessment(
            task_id=task.task_id,
            primary_domain=primary.name,
            secondary_domains=secondary,
            task_type=self._resolve_task_type(task.task_type, text),
            risk_level=risk,
            identified_standards=standards,
            recommended_source_types=source_types,
            recommended_evaluation_criteria=criteria,
            uncertainties=uncertainties,
        )

    @classmethod
    def _resolve_task_type(cls, current: str, text: str) -> str:
        if current.casefold() not in cls.GENERIC_TASK_TYPES:
            return current
        if any(token in text for token in ("compare", "comparison", "versus", " vs ", "порівн")):
            return "comparative_analysis"
        if any(token in text for token in ("recommend", "recommendation", "рекоменд")):
            return "recommendation"
        if any(token in text for token in ("calculate", "estimate", "assess", "evaluate", "розрах", "оцін")):
            return "assessment"
        if any(token in text for token in ("explain", "поясн")):
            return "explanatory_research"
        return "research"

    @staticmethod
    def _risk_rank(level: RiskLevel) -> int:
        return {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4,
        }[level]

    @staticmethod
    def _dedupe(values) -> list[str]:
        return list(dict.fromkeys(values))
