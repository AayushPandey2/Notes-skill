"""Educational obligations and adaptive laboratory/assessment policy.

Operates on the Writer's Composition record; does not own a second plan,
prose generator, mathematical engine, asset store or completion ledger.
"""
from __future__ import annotations

import re
from scriptorium.models import content_hash

QUESTIONS = {
    'what': 'meaning, definition and components',
    'why': 'motivating problem and purpose',
    'how': 'causal mechanism and intermediate reasoning',
    'when_use': 'appropriate conditions and selection criteria',
    'when_not_use': 'limitations, violated assumptions and alternatives',
    'apply': 'worked application or reproducible procedure',
}
PROGRESSION = ('why', 'intuition', 'prerequisites', 'what', 'how', 'mathematics',
               'example', 'visual', 'apply', 'when_use', 'when_not_use', 'reinforcement')
LAB_STAGES = {
    'problem': 'Problem and success criteria', 'environment': 'Environment and prerequisites',
    'acquisition': 'Data, materials or source acquisition', 'exploration': 'Initial exploration',
    'preprocessing': 'Transformations and preparation', 'workflow': 'Reusable workflow',
    'implementation': 'Core implementation or procedure', 'optimization': 'Optimization and tuning',
    'evaluation': 'Evaluation', 'debugging': 'Debugging and failure analysis',
    'end_to_end': 'Complete end-to-end example', 'challenge': 'Independent practice',
}
LAB_DOMAINS = {
    'programming': {'problem','environment','workflow','implementation','evaluation','debugging','end_to_end','challenge'},
    'machine_learning': set(LAB_STAGES),
    'mathematics': {'problem','environment','exploration','workflow','implementation','evaluation','debugging','end_to_end','challenge'},
    'experimental': set(LAB_STAGES)-{'optimization'},
    'humanities': {'problem','environment','acquisition','exploration','workflow','implementation','evaluation','end_to_end','challenge'},
    'general': {'problem','environment','implementation','evaluation','end_to_end','challenge'},
}
ASSESSMENT_TYPES = {
    'conceptual', 'mathematical', 'numerical', 'practical', 'comparison',
    'diagnosis', 'transfer', 'critical', 'algorithmic', 'implementation',
    'historical', 'causal', 'experimental_design',
}
VISUAL_ROLES = ('overview', 'motivation', 'mechanism', 'mathematical', 'worked_example', 'comparison', 'application', 'synthesis')
_GENERIC_COMPARISON_RE = re.compile(r'\bOption\s+[AB]\b', re.I)


def text(value):
    if isinstance(value, list):
        return '\n\n'.join(text(item) for item in value)
    if isinstance(value, dict):
        return str(value.get('text') or '')
    return str(value or '').strip()


def substantive(value):
    value = text(value)
    prose = re.sub(r'^\s*#{1,6}[^\n]*$', '', value, flags=re.M).strip()
    return (
        bool(prose)
        and not re.search(r'\b(?:TODO|TBD|FIXME)\b|\[placeholder\]|^(?:explain|describe|insert) (?:this|the concept)\b', prose, re.I)
        and not _GENERIC_COMPARISON_RE.search(prose)
    )


def _present_in_body(value, body: str, dequoted_body: str | None = None) -> bool:
    """Check that substantive content appears in body, including multiline blockquoted callouts."""
    if not substantive(value):
        return False
    raw = text(value)
    if raw in body:
        return True
    dq = dequoted_body if dequoted_body is not None else re.sub(r'(?m)^>\s?', '', body)
    return raw in dq


def configure(plan, extension, context):
    """Populate obligations on the existing contract from explicit instructional demands."""
    plan.teaching = dict(extension.get('teaching') or {})
    unknown = set(plan.teaching) - set(QUESTIONS) - {'intuition', 'reinforcement'}
    if unknown:
        raise ValueError('Unknown teaching roles: ' + ', '.join(sorted(unknown)))
    plan.bindings = dict(extension.get('teaching_bindings') or {})
    if set(plan.bindings) - set(QUESTIONS):
        raise ValueError('Teaching bindings must name the six canonical questions')
    plan.mechanism = dict(extension.get('mechanism') or {})
    plan.depth_profile = dict(extension.get('depth_profile') or {})
    complexity = plan.depth_profile.get('complexity', context.get('complexity', 'standard'))
    if complexity not in {'trivial', 'simple', 'standard', 'complex'}:
        raise ValueError('Complexity must be trivial, simple, standard or complex')
    plan.practical = dict(extension.get('practical') or {})

    reasons: dict[str, str] = {}
    def _req(key: str, reason: str) -> None:
        if key not in reasons:
            reasons[key] = reason

    _req('orientation', 'Every concept needs a motivating starting problem before formalism')
    _req('mechanism', 'Core causal mechanism must be explained step by step')
    substantial = complexity != 'trivial' and plan.master not in {'M3', 'M6'}
    if substantial:
        for q, desc in QUESTIONS.items():
            _req(q, desc)
        _req('example', 'Substantial concepts require a worked or practical demonstration')
        _req('interpretation', 'Results must be interpreted in context')
        _req('limitations', 'Applicability boundaries and violated assumptions must be stated')
    elif plan.master != 'M6':
        _req('what', QUESTIONS['what'])

    if plan.audience in {'beginner', 'comprehensive'} and plan.master not in {'M3', 'M6'}:
        _req('intuition', f"Audience '{plan.audience}' requires an intuitive mental model before formalism")
    if plan.prerequisites or plan.depth_profile.get('prerequisite_burden', 0) > 0:
        _req('prerequisites', 'Prerequisite bridges required before dependent concepts')
    if plan.mathematics or plan.depth_profile.get('mathematical_difficulty', 0) >= 2:
        _req('formula_folds', 'Displayed equations require adjacent 12-stage collapsed explanations')
    if any(str(goal).lower().startswith(('derive', 'prove')) for goal in plan.objectives):
        _req('mathematical_reasoning', 'Derivation/proof objective requires intermediate mathematical steps')
    if any(str(goal).lower().startswith(('calculate', 'compute', 'solve')) for goal in plan.objectives):
        _req('numerical_reasoning', 'Calculation/solve objective requires explicit numerical walkthrough')
    if plan.mechanism or plan.depth_profile.get('internal_mechanisms', 0) >= 1:
        _req('mechanism_reconstruction', 'Explicit input -> step -> output mechanism reconstruction required')
    if complexity == 'complex' or plan.depth_profile.get('advanced_connections'):
        _req('advanced_connection', 'Complex or connected concepts require explicit downstream links')
        _req('assessment_alignment', 'Complex concepts require objective-aligned assessment checks')
    if plan.practical or plan.depth_profile.get('implementation_importance', 0) >= 2:
        _req('practical_quality', 'Practical/implementation demand requires reproducible lab stages')
    if extension.get('visual_requirements') or plan.assets:
        _req('visual_roles', 'Declared visual roles require verified local assets and hash-bound inspections')
    if extension.get('comparisons'):
        _req('comparative_reasoning', 'Method selection requires causal comparison prose before summary tables')
    if extension.get('misconceptions'):
        _req('limitations', 'Explicit misconceptions and failure boundaries must be addressed')
    if plan.assessments:
        _req('assessment_alignment', 'Supplied assessments must align with declared learning objectives')

    plan.obligations = dict.fromkeys(reasons, 'pending')
    plan.obligation_details = {
        key: {'reason': reason, 'evidence': [], 'deficiencies': []}
        for key, reason in reasons.items()
    }
    if extension.get('teaching') or plan.practical or extension.get('visual_requirements'):
        plan.record(
            'composition.learning.configure',
            complexity=complexity,
            questions=list(QUESTIONS) if substantial else ['what'],
            practical_domain=plan.practical.get('domain'),
            progression=list(PROGRESSION),
        )


def mechanism_text(mechanism):
    if not mechanism:
        return ''
    sections = []
    if mechanism.get('inputs'):
        sections.append('Inputs: '+text(mechanism['inputs']))
    for index, step in enumerate(mechanism.get('steps',[]),1):
        sections.append(f"{index}. **{step.get('component','Step')}:** {text(step.get('receives'))} "
                        f"{text(step.get('operation'))} {text(step.get('reason'))} "
                        f"{text(step.get('produces'))} {text(step.get('next'))}")
    if mechanism.get('outputs'):
        sections.append('Output: '+text(mechanism['outputs']))
    if mechanism.get('interpretation'):
        sections.append(text(mechanism['interpretation']))
    return '\n\n'.join(sections)


def practical_requirements(practical):
    domain = practical.get('domain','general')
    if domain not in LAB_DOMAINS:
        raise ValueError('Unknown laboratory domain: '+str(domain))
    supplied = practical.get('stages',{})
    if not isinstance(supplied,dict) or set(supplied)-set(LAB_STAGES):
        raise ValueError('Laboratory stages must use the canonical twelve stage keys')
    active = LAB_DOMAINS[domain] | set(supplied)
    return domain, active


def render_practical(plan):
    if not plan.practical:
        return ''
    domain, active = practical_requirements(plan.practical)
    stages = plan.practical.get('stages',{})
    lines = []
    for key, title in LAB_STAGES.items():
        if key in active and substantive(stages.get(key)):
            lines += ['### '+title, '', text(stages[key]), '']
        if key=='implementation' and plan.practical.get('code'):
            language = plan.practical.get('language','python')
            if not re.fullmatch(r'[a-zA-Z0-9_+.-]+',language) or '```' in plan.practical['code']:
                raise ValueError('Invalid practical code fence or nested fence')
            lines += [f'```{language}',plan.practical['code'].rstrip(),'```','']
    plan.record('composition.learning.render_practical',domain=domain,active_stages=sorted(active))
    return '\n'.join(lines)


def render_assessments(plan):
    questions=[]
    for index, question in enumerate(plan.assessments,1):
        if not question.get('question') or not question.get('answer'):
            raise ValueError('Assessment requires an actual question and answer')
        lines=[f'### Question {index}', '',str(question['question']),'']
        if question.get('hint'):
            lines += ['> [!hint]- Hint', '> '+text(question['hint']).replace('\n','\n> '),'']
        answer = '\n\n'.join(value for value in [text(question.get('reasoning')),text(question['answer'])] if value)
        lines += ['> [!tip]- Answer', '> '+answer.replace('\n','\n> '),'']
        questions.append('\n'.join(lines))
    plan.record('composition.learning.render_assessments',count=len(questions))
    return '\n\n'.join(questions)


def verify(plan, body):
    """Check concrete evidence in produced content; do not infer semantic truth from headings."""
    from ..mathematics import validate_formula_folds
    headings = {heading: content for heading, content in plan.sections}
    dequoted = re.sub(r'(?m)^>\s?', '', body)
    content = lambda value: _present_in_body(value, body, dequoted)
    supplied = {role: text(value) for role, value in plan.teaching.items()}
    for role, heading in plan.bindings.items():
        supplied[role] = headings.get(heading, '')
    evidence = {role: content(supplied.get(role)) for role in QUESTIONS}
    # Legacy headings remain readable input bindings; no alternative Writer is invoked.
    evidence.update({
        'orientation': evidence['why'] or content(headings.get('Why This Matters & Starting Problem')) or content(headings.get('Source Context & Overview')) or content(headings.get('Core Reference')),
        'mechanism': evidence['how'] or content(headings.get('How the Mechanism Works')) or content(headings.get('Sequential Development')),
        'intuition': content(plan.teaching.get('intuition')) or content(headings.get('Intuitive Picture Before Any Formalism')),
        'example': bool(plan.examples) or bool(plan.practical) or content(supplied.get('apply')) or content(headings.get('Step-by-Step State Evolution')),
        'interpretation': content(plan.teaching.get('reinforcement')) or content(headings.get('Reconstructing the Reasoning')),
        'limitations': evidence['when_not_use'] or content(headings.get('Applicability Conditions, Misconceptions, and Distinctions')),
        'prerequisites': content(headings.get('Building the Needed Foundations')),
        'mathematical_reasoning': bool(plan.mathematics) and all(substantive(e.get('derivation_reasoning')) for e in plan.mathematics),
        'numerical_reasoning': bool(plan.examples) or any(e.get('numerical_example', {}).get('steps') for e in plan.mathematics),
        'advanced_connection': content(headings.get('Next Connection')),
        'comparative_reasoning': any(
            ('Comparing Alternatives' in h or re.search(r'\bvs\.?\b|\bcomparison\b', h, re.I)) and substantive(c)
            for h, c in plan.sections
        ),
    })
    math = validate_formula_folds(body, learner_level=plan.audience)
    evidence['formula_folds'] = math['passed']
    deficiencies = []
    mechanism_errors = []
    if plan.mechanism:
        for key in ('inputs', 'outputs', 'interpretation'):
            if not substantive(plan.mechanism.get(key)):
                mechanism_errors.append('Mechanism missing ' + key)
        if not plan.mechanism.get('steps'):
            mechanism_errors.append('Mechanism has no intermediate operations')
        for index, step in enumerate(plan.mechanism.get('steps', []), 1):
            for key in ('component', 'receives', 'operation', 'reason', 'produces', 'next'):
                if not substantive(step.get(key)):
                    mechanism_errors.append(f'Mechanism step {index} missing {key}')
        if mechanism_text(plan.mechanism) not in body:
            mechanism_errors.append('Mechanism record is absent from generated prose')
    else:
        mechanism_errors.append('No explicit mechanism reconstruction record')
    evidence['mechanism_reconstruction'] = not mechanism_errors

    visual_errors = []
    declared_roles = [
        r.get('role') for r in (getattr(plan, 'visual_requirements', None) or [])
        if isinstance(r, dict) and r.get('role')
    ]
    for role in declared_roles:
        if role not in VISUAL_ROLES:
            visual_errors.append(f'Unknown visual role: {role}')
    if plan.assets:
        if len(plan.inspections) != len(plan.assets):
            visual_errors.append('Every acquired asset requires a matching inspection record')
        for asset, insp in zip(plan.assets, plan.inspections):
            if not insp.get('inspection_performed') or asset.get('hash') != insp.get('content_hash'):
                visual_errors.append('Asset/inspection hash mismatch')
    elif declared_roles:
        visual_errors.append('Declared visual roles lack verified acquired assets')
    evidence['visual_roles'] = not visual_errors

    lab_errors = []
    stage_status = {}
    if plan.practical:
        domain, active = practical_requirements(plan.practical)
        for key in LAB_STAGES:
            value = plan.practical.get('stages', {}).get(key)
            omission = plan.practical.get('omissions', {}).get(key)
            if content(value):
                stage_status[key] = 'generated'
            elif key not in active:
                stage_status[key] = 'not_applicable'
            elif substantive(omission):
                stage_status[key] = 'justifiably_omitted'
            else:
                stage_status[key] = 'pending'
                lab_errors.append('Laboratory missing ' + key)
        code = plan.practical.get('code')
        if code:
            receipt = plan.practical.get('execution', {})
            if not (receipt.get('code_sha256') == content_hash(code) and receipt.get('status') == 'passed'
                    and 'expected' in receipt and receipt.get('expected') == receipt.get('observed') and receipt.get('method')):
                lab_errors.append('Practical code lacks a matching recorded execution result')
            if code not in body:
                lab_errors.append('Practical implementation is absent from output')
    evidence['practical_quality'] = bool(plan.practical) and not lab_errors
    assessment_errors = []
    kinds = set()
    ids = set()
    for index, item in enumerate(plan.assessments):
        qid = item.get('id', str(index))
        if qid in ids:
            assessment_errors.append('Duplicate assessment identity ' + str(qid))
        ids.add(qid)
        if item.get('type') not in ASSESSMENT_TYPES:
            assessment_errors.append(f'Question {qid} lacks a supported type')
        kinds.add(item.get('type'))
        objectives = item.get('objectives', [])
        if not objectives or set(objectives) - set(plan.objectives):
            assessment_errors.append(f'Question {qid} does not align to declared objectives')
        for key in ('question', 'hint', 'reasoning', 'answer'):
            if not content(item.get(key)):
                assessment_errors.append(f'Question {qid} missing published {key}')
    required_types = set(plan.depth_profile.get('assessment_types', []))
    if required_types - kinds:
        assessment_errors.append('Requested assessment diversity missing: ' + ', '.join(sorted(required_types - kinds)))
    evidence['assessment_alignment'] = bool(plan.assessments) and not assessment_errors
    for key in plan.obligations:
        plan.obligations[key] = 'generated' if evidence.get(key) else 'pending'
        detail = plan.obligation_details[key]
        detail['evidence'] = [supplied[key]] if key in supplied and evidence.get(key) else []
        detail['deficiencies'] = [] if evidence.get(key) else ['Missing actual content for ' + detail['reason']]
        if not evidence.get(key):
            deficiencies.append({'obligation': key, 'detail': detail['deficiencies'][0]})
    domains = {
        'conceptual': {'deficiencies': [d for d in deficiencies if d['obligation'] in QUESTIONS]},
        'mathematical': {'deficiencies': math['issues']},
        'visual': {'deficiencies': visual_errors},
        'practical': {'deficiencies': lab_errors, 'stages': stage_status},
        'teaching': {'deficiencies': mechanism_errors if 'mechanism_reconstruction' in plan.obligations else []},
        'assessment': {'deficiencies': assessment_errors if plan.assessments else []},
    }
    return {
        'complete': all(status != 'pending' for status in plan.obligations.values()) and math['passed'],
        'obligations': dict(plan.obligations),
        'obligation_details': plan.obligation_details,
        'mathematics': math,
        'deficiencies': deficiencies,
        'dimensions': domains,
        'scope': 'Content-bound structural and numerical checks; semantic accuracy, execution receipts and image interpretation require scoped evidence review.',
    }


def build_remediation(plan, responses: list[dict]) -> dict:
    """Generate targeted remediation strictly from actual supplied learner responses.

    Never invents learner responses, mastery scores, or unverified misconceptions.
    """
    if not isinstance(responses, list) or not responses:
        return {
            'status': 'no_learner_responses',
            'remediation': [],
            'note': 'Static questions alone do not measure learner understanding; supply actual learner responses.',
        }
    by_id = {str(item.get('id', i)): item for i, item in enumerate(plan.assessments)}
    remediation: list[dict] = []
    for resp in responses:
        if not isinstance(resp, dict) or 'question_id' not in resp or 'correct' not in resp:
            raise ValueError('Each learner response requires question_id and boolean correct')
        qid = str(resp['question_id'])
        if qid not in by_id:
            raise ValueError(f'Unknown question_id in learner response: {qid}')
        if resp['correct'] is False:
            q = by_id[qid]
            remediation.append({
                'question_id': qid,
                'objectives': list(q.get('objectives', [])),
                'hint': text(q.get('hint')),
                'reasoning': text(q.get('reasoning')),
                'learner_answer': str(resp.get('answer', '')),
            })
    return {
        'status': 'remediation_generated' if remediation else 'all_correct',
        'responses_evaluated': len(responses),
        'remediation': remediation,
    }
