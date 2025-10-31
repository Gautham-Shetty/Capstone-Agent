from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine, OperatorConfig
from typing import Tuple, Dict

_analyzer = AnalyzerEngine()
_anonymizer = AnonymizerEngine()

def redact_text(text:str,language:str="en")->Tuple[str,Dict]:
    results=_analyzer.analyze(text=text,language=language)
    if not results:
        return text,{}
    anonymized_result=_anonymizer.anonymize(text=text,analyzer_results=results)
    report = {"entities": [{"entity_type": r.entity_type, "start": r.start, "end": r.end} for r in results]}
    return anonymized_result.text,report