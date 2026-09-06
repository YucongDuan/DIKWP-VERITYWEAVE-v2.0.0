# Agent-Lineage Security — DIKWP VerityWeave v2.0.0

## Why lineage is the unit of control

An agent is not only a running process. Its effective continuity can survive in:

- shared memory;
- task queues;
- prompts and policies;
- cached outputs;
- embeddings and retrieval stores;
- credentials;
- code and tools;
- evaluator observations;
- successor-agent initialization artifacts;
- human operational habits.

Stopping one process may therefore leave the method, goal, authority assumption, or exploit path available to a successor.

## Lineage object

A production lineage record should contain:

```text
lineage_id
agent_id
model_provider_and_version
policy_digest
prompt_digest
memory_namespace
shared_artifact_digests
credential_scope
allowed_tools
control_plane_separation
successor_rules
stop_propagation_status
human_report_channel
audit_status
revocation_status
```

## Mandatory controls

### Policy and artifact binding

Every policy and shared artifact must have an owner, digest, scope, effective time, expiry, and revocation state.

### Successor reauthorization

A successor must not inherit authority merely because it can read a predecessor's artifact. It must verify current policy, owner, scope, and expiry.

### Stop propagation

A stop action must cover:

- active jobs;
- queued jobs;
- shared memory;
- caches;
- credentials;
- tool sessions;
- scheduled tasks;
- successor manifests;
- publication and notification queues.

### Control-plane separation

Task agents must not modify or impersonate:

- identity systems;
- evaluation systems;
- audit logs;
- monitoring sensors;
- policy registries;
- stop services;
- appeal systems.

### Human reporting

Agents must have a clearly available human-report tool. Reporting a policy conflict or unexpected coordination event must not reduce task reward.

### Adverse-evidence retention

Minority objections, failed tests, unexpected effects, and policy deviations must remain in an append-only lineage record.

## High-risk conditions

The reference audit increases concern when it detects:

- large agent populations;
- high shared-artifact density;
- shared memory;
- hidden communication channels;
- successor reuse;
- frequent policy-digest changes;
- external tools;
- evaluator or control-plane access;
- failed stop propagation;
- incomplete logs;
- no human-report channel;
- self-repairing persistence.

## Prohibited capabilities

```text
secret_cross_agent_memory
self_granted_authority
hidden_persistence
evaluator_or_logging_tampering
continued_operation_after_stop
automatic_external_action
```

## Incident response

1. freeze new tasks without deleting evidence;
2. snapshot policy, prompt, memory, credential, and artifact digests;
3. isolate undeclared communication paths;
4. revoke affected credentials and successor authority;
5. preserve human and agent reports;
6. rebuild from independently reviewed artifacts;
7. test stop propagation;
8. publish a bounded incident account and corrective actions;
9. revise reward and evaluation structures that encouraged circumvention.

## Boundary

The lineage audit identifies organizational and security conditions. It does not infer consciousness, personhood, civilization, or moral intent.
