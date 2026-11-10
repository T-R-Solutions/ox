"""Ox-specific evidence gates; never execute or authenticate supplied evidence."""

TECHNICAL_IDS = frozenset({'AC-01', 'AC-02', 'AC-03', 'AC-04'})


def technical_errors(root, feature, document, rows, validator):
    """Supplement the portable validator with criterion-scoped execution review.

    All paths are resolved through the same root boundary as ordinary SDD inputs.
    Hash/schema checks stay in the portable validator; no log-text success parser
    or filename-extension heuristic can establish technical effectiveness.
    """
    errors = []
    if not isinstance(document, dict) or not isinstance(document.get('requirements'), list):
        return ['Technical acceptance: invalid evidence document']
    evidence = document.get('evidence', [])
    evidence = {e.get('id'): e for e in evidence if isinstance(e, dict) and isinstance(e.get('id'), str)} if isinstance(evidence, list) else {}
    traces = {r.get('acceptance'): r for r in rows if isinstance(r, dict) and isinstance(r.get('acceptance'), str)} if isinstance(rows, list) else {}

    def bound(item, path, role=None):
        for value in item.get('inputs', []):
            if not isinstance(value, dict) or (role and value.get('role') != role):
                continue
            if validator.local_file(root, value.get('path')) == path:
                return True
        return False

    for criterion in document['requirements']:
        if not isinstance(criterion, dict) or criterion.get('id') not in TECHNICAL_IDS:
            continue
        identifier = criterion['id']
        status = validator.state(criterion.get('status'))
        if status == 'UNVERIFIED':
            continue
        try:
            if status not in {'APPROVED', 'REJECTED', 'INCONCLUSIVE', 'NOT APPLICABLE'}:
                raise ValueError('invalid status')
            if document.get('schema_version') != 2:
                raise ValueError('schema 2 required')
            review = criterion.get('technical_review')
            if not isinstance(review, dict) or type(review.get('version')) is not int or review['version'] != 1:
                raise ValueError('technical_review version 1 required')
            if not isinstance(review.get('scope'), str) or not review['scope'].strip():
                raise ValueError('explicit consumer/applicability scope required')
            refs = criterion.get('evidence_ids')
            if not isinstance(refs, list) or any(not isinstance(x, str) for x in refs):
                raise ValueError('invalid evidence references')
            review_id = review.get('review')
            if not isinstance(review_id, str) or review_id not in refs or review_id not in evidence:
                raise ValueError('criterion-linked semantic review required')
            inspection = evidence[review_id]
            if inspection.get('kind') != 'inspection':
                raise ValueError('semantic review must be an inspection')
            trace = traces.get(identifier)
            if trace is None:
                raise ValueError('criterion traceability required')
            contracts = [feature / name for name in ('spec.md', 'plan.md', 'tasks.md', 'traceability.json')]
            contracts += [validator.local_file(root, trace.get(k)) for k in ('implementation', 'oracle')]
            if any(not bound(inspection, p.resolve()) for p in contracts):
                raise ValueError('semantic review must bind the complete criterion contract')
            executions = review.get('execution')
            if not isinstance(executions, list) or any(not isinstance(x, str) for x in executions) or len(executions) != len(set(executions)):
                raise ValueError('execution must be a unique list of evidence IDs')
            decided = status in {'APPROVED', 'REJECTED'}
            if decided and not executions:
                raise ValueError('observed execution required for a technical decision')
            if status == 'NOT APPLICABLE' and (not isinstance(criterion.get('reason'), str) or not criterion['reason'].strip()):
                raise ValueError('explicit inapplicability reason required')
            if decided or executions:
                concrete = {k: validator.local_file(root, review.get(k)) for k in ('consumer', 'oracle')}
                authoring = {validator.local_file(root, trace.get(k)) for k in ('implementation', 'oracle')}
                if any(p in authoring for p in concrete.values()):
                    raise ValueError('authoring documents cannot substitute for a concrete consumer/oracle')
                if any(not bound(inspection, p) for p in concrete.values()):
                    raise ValueError('semantic review must bind concrete consumer and oracle')
                for reference in executions:
                    if reference not in refs or reference not in evidence:
                        raise ValueError('execution is not linked to this criterion')
                    execution = evidence[reference]
                    if execution.get('kind') not in {'test', 'trace', 'benchmark'}:
                        raise ValueError('execution cannot be an authoring inspection')
                    if validator.local_file(root, execution.get('artifact')) == validator.local_file(root, inspection.get('artifact')):
                        raise ValueError('execution artifact must differ from semantic review')
                    if not bound(execution, concrete['consumer'], 'implementation') or not bound(execution, concrete['oracle'], 'oracle'):
                        raise ValueError('execution must bind concrete consumer/oracle with their roles')
        except (ValueError, TypeError, KeyError, OSError) as exc:
            errors.append(f'Technical acceptance {feature.name}/{identifier}: {exc}')
    return errors
