use chrono::{DateTime, Utc};
use fabric_authority::{AuthorityDecision, AuthorityResult};
use fabric_core::{FabricId, ReconciliationDecision, RiskLevel};
use fabric_validate::{ValidationReport, ValidationSeverity};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum DriftKind {
    MissingNode,
    MissingRelationship,
    MissingIdentity,
    MissingEvidence,
    MissingContract,
    PolicyDrift,
    RuntimeDrift,
    AuthorityDrift,
    TrustDrift,
    SchemaDrift,
    ConflictDrift,
    OrphanDrift,
    TimingDrift,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DriftRecord {
    pub id: FabricId,
    pub target: FabricId,
    pub kind: DriftKind,
    pub severity: RiskLevel,
    pub evidence: Vec<FabricId>,
    pub detected_at: DateTime<Utc>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ReconciliationInput {
    pub id: FabricId,
    pub target: FabricId,
    pub desired_state: FabricId,
    pub observed_state: FabricId,
    pub current_state: FabricId,
    pub validation: ValidationReport,
    pub authority: AuthorityResult,
    pub evidence: Vec<FabricId>,
    pub risk: RiskLevel,
    pub drift: Option<DriftRecord>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ReconciliationPlan {
    pub id: FabricId,
    pub target: FabricId,
    pub decision: ReconciliationDecision,
    pub reason: String,
    pub required_actions: Vec<String>,
    pub created_at: DateTime<Utc>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ReconciliationOutcome {
    pub id: FabricId,
    pub input: FabricId,
    pub plan: ReconciliationPlan,
    pub applied_changes: Vec<FabricId>,
    pub resulting_state: Option<FabricId>,
    pub completed_at: DateTime<Utc>,
}

pub trait Reconciler {
    fn plan(&self, input: &ReconciliationInput) -> ReconciliationPlan;

    fn reconcile(&self, input: &ReconciliationInput) -> ReconciliationOutcome {
        let plan = self.plan(input);
        ReconciliationOutcome {
            id: format!("reconciliation-outcome:{}", input.id),
            input: input.id.clone(),
            applied_changes: vec![],
            resulting_state: None,
            completed_at: Utc::now(),
            plan,
        }
    }
}

pub trait DriftDetector<T> {
    fn detect_drift(&self, target: &T) -> Vec<DriftRecord>;
}

pub trait GapResolver<T> {
    fn resolve_gap(&self, drift: &DriftRecord, target: &T) -> Option<FabricId>;
}

pub trait ConflictResolver<T> {
    fn resolve_conflict(&self, drift: &DriftRecord, target: &T) -> Option<FabricId>;
}

pub trait StateResolver<T> {
    fn desired_state_for(&self, target: &T) -> Option<FabricId>;
    fn observed_state_for(&self, target: &T) -> Option<FabricId>;
    fn current_state_for(&self, target: &T) -> Option<FabricId>;
}

#[derive(Debug, Default, Clone)]
pub struct BasicReconciler;

impl Reconciler for BasicReconciler {
    fn plan(&self, input: &ReconciliationInput) -> ReconciliationPlan {
        let now = Utc::now();

        if input.evidence.is_empty() {
            return ReconciliationPlan {
                id: format!("reconciliation-plan:{}", input.id),
                target: input.target.clone(),
                decision: ReconciliationDecision::NeedsEvidence,
                reason: "Reconciliation requires at least one evidence reference.".to_string(),
                required_actions: vec!["attach_evidence".to_string()],
                created_at: now,
            };
        }

        if !input.validation.valid {
            let has_critical = input
                .validation
                .issues
                .iter()
                .any(|issue| issue.severity == ValidationSeverity::Critical);

            return ReconciliationPlan {
                id: format!("reconciliation-plan:{}", input.id),
                target: input.target.clone(),
                decision: if has_critical {
                    ReconciliationDecision::Quarantine
                } else {
                    ReconciliationDecision::Rejected
                },
                reason: "Validation failed.".to_string(),
                required_actions: vec!["fix_validation_errors".to_string()],
                created_at: now,
            };
        }

        match input.authority.decision {
            AuthorityDecision::Permit => {
                if input.risk == RiskLevel::Critical {
                    ReconciliationPlan {
                        id: format!("reconciliation-plan:{}", input.id),
                        target: input.target.clone(),
                        decision: ReconciliationDecision::Escalate,
                        reason: "Critical-risk reconciliation requires explicit final review.".to_string(),
                        required_actions: vec!["final_human_or_platform_review".to_string()],
                        created_at: now,
                    }
                } else {
                    ReconciliationPlan {
                        id: format!("reconciliation-plan:{}", input.id),
                        target: input.target.clone(),
                        decision: ReconciliationDecision::Accepted,
                        reason: "Validation passed and authority permitted the change.".to_string(),
                        required_actions: vec![],
                        created_at: now,
                    }
                }
            }
            AuthorityDecision::RequireEvidence => ReconciliationPlan {
                id: format!("reconciliation-plan:{}", input.id),
                target: input.target.clone(),
                decision: ReconciliationDecision::NeedsEvidence,
                reason: "Authority engine requires additional evidence.".to_string(),
                required_actions: vec!["attach_authority_evidence".to_string()],
                created_at: now,
            },
            AuthorityDecision::RequireAuthority => ReconciliationPlan {
                id: format!("reconciliation-plan:{}", input.id),
                target: input.target.clone(),
                decision: ReconciliationDecision::NeedsAuthority,
                reason: "Authority chain is incomplete.".to_string(),
                required_actions: vec!["complete_authority_chain".to_string()],
                created_at: now,
            },
            AuthorityDecision::Expired => ReconciliationPlan {
                id: format!("reconciliation-plan:{}", input.id),
                target: input.target.clone(),
                decision: ReconciliationDecision::NeedsAuthority,
                reason: "Authority grant or delegation expired.".to_string(),
                required_actions: vec!["renew_authority".to_string()],
                created_at: now,
            },
            AuthorityDecision::Escalate => ReconciliationPlan {
                id: format!("reconciliation-plan:{}", input.id),
                target: input.target.clone(),
                decision: ReconciliationDecision::Escalate,
                reason: "Authority engine requested escalation.".to_string(),
                required_actions: vec!["escalate_to_accountable_authority".to_string()],
                created_at: now,
            },
            AuthorityDecision::Deny => ReconciliationPlan {
                id: format!("reconciliation-plan:{}", input.id),
                target: input.target.clone(),
                decision: ReconciliationDecision::Rejected,
                reason: "Authority denied the change.".to_string(),
                required_actions: vec!["request_authority_or_reject".to_string()],
                created_at: now,
            },
        }
    }
}
