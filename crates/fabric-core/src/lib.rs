use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use serde_json::Value;

pub type FabricId = String;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum LifecycleStatus {
    Draft,
    Proposed,
    Validating,
    NeedsEvidence,
    NeedsAuthority,
    NeedsContract,
    Approved,
    Active,
    Degraded,
    Challenged,
    Quarantined,
    Suspended,
    Superseded,
    Retired,
    Archived,
    Rejected,
    Failed,
    Expired,
    Violated,
    Fulfilled,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum RiskLevel {
    Low,
    Medium,
    High,
    Critical,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum NodeType {
    Human,
    Agent,
    Tool,
    Skill,
    Model,
    Runtime,
    Kernel,
    Workspace,
    Policy,
    Organization,
    Team,
    Document,
    Decision,
    Contract,
    Service,
    System,
    Resource,
    Event,
    Trace,
    Proposal,
    Reconciliation,
    State,
    DigitalTwin,
    FabricFederation,
    FabricDomain,
    FabricCluster,
    FabricBox,
    FabricParticipant,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum Predicate {
    IsA,
    OwnedBy,
    OperatedBy,
    ControlledBy,
    GovernedBy,
    AuthorizedBy,
    Uses,
    DependsOn,
    RunsOn,
    BelongsTo,
    Contains,
    Produces,
    Consumes,
    Observes,
    Emits,
    TracedBy,
    EvidencedBy,
    Trusts,
    DelegatesTo,
    ReportsTo,
    ContractsWith,
    BoundBy,
    Reconciles,
    Approves,
    Rejects,
    Proposes,
    Requires,
    Satisfies,
    Violates,
    ConflictsWith,
    Supersedes,
    DerivedFrom,
    Mirrors,
    Represents,
    ManagedBy,
    ParticipatesIn,
    FederatesWith,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum AuthorityKind {
    System,
    Agent,
    Policy,
    Human,
    Platform,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TemporalContext {
    pub observed_at: Option<DateTime<Utc>>,
    pub recorded_at: DateTime<Utc>,
    pub effective_at: Option<DateTime<Utc>>,
    pub valid_from: Option<DateTime<Utc>>,
    pub valid_to: Option<DateTime<Utc>>,
    pub expires_at: Option<DateTime<Utc>>,
    pub superseded_at: Option<DateTime<Utc>>,
    pub reconciled_at: Option<DateTime<Utc>>,
    pub projected_at: Option<DateTime<Utc>>,
}

impl TemporalContext {
    pub fn now() -> Self {
        Self {
            observed_at: Some(Utc::now()),
            recorded_at: Utc::now(),
            effective_at: None,
            valid_from: None,
            valid_to: None,
            expires_at: None,
            superseded_at: None,
            reconciled_at: None,
            projected_at: None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Node {
    pub id: FabricId,
    pub node_type: NodeType,
    pub name: String,
    pub status: LifecycleStatus,
    pub temporal: TemporalContext,
    pub metadata: Value,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Relationship {
    pub id: FabricId,
    pub subject: FabricId,
    pub predicate: Predicate,
    pub object: FabricId,
    pub status: LifecycleStatus,
    pub authority: AuthorityKind,
    pub risk: RiskLevel,
    pub evidence: Vec<FabricId>,
    pub temporal: TemporalContext,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Intent {
    pub id: FabricId,
    pub expressed_by: FabricId,
    pub scope: FabricId,
    pub purpose: String,
    pub objectives: Vec<FabricId>,
    pub constraints: Vec<FabricId>,
    pub success_criteria: Vec<FabricId>,
    pub risk: RiskLevel,
    pub status: LifecycleStatus,
    pub temporal: TemporalContext,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Event {
    pub id: FabricId,
    pub event_type: String,
    pub subject: FabricId,
    pub source: FabricId,
    pub payload: Value,
    pub temporal: TemporalContext,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Trace {
    pub id: FabricId,
    pub subject: FabricId,
    pub source: FabricId,
    pub evidence_type: String,
    pub hash: Option<String>,
    pub temporal: TemporalContext,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CommitmentRecord {
    pub id: FabricId,
    pub debtor: FabricId,
    pub creditor: FabricId,
    pub scope: String,
    pub condition: String,
    pub obligations: Vec<String>,
    pub constraints: Vec<FabricId>,
    pub due_at: Option<DateTime<Utc>>,
    pub status: LifecycleStatus,
    pub evidence: Vec<FabricId>,
    pub authority_chain: Option<FabricId>,
    pub temporal: TemporalContext,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AuthorityChain {
    pub id: FabricId,
    pub target: FabricId,
    pub observer: FabricId,
    pub proposer: FabricId,
    pub validator: FabricId,
    pub reviewers: Vec<FabricId>,
    pub approvers: Vec<FabricId>,
    pub reconciler: FabricId,
    pub state_projector: Option<FabricId>,
    pub accountable_authority: FabricId,
    pub risk: RiskLevel,
    pub status: LifecycleStatus,
    pub trace: FabricId,
    pub temporal: TemporalContext,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum GapType {
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
    VocabularyGap,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct GapFillProposal {
    pub id: FabricId,
    pub gap_type: GapType,
    pub subject: FabricId,
    pub proposed_change: Value,
    pub confidence: f64,
    pub risk: RiskLevel,
    pub evidence: Vec<FabricId>,
    pub proposed_by: FabricId,
    pub approval_required: bool,
    pub status: LifecycleStatus,
    pub temporal: TemporalContext,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum ReconciliationDecision {
    Accepted,
    Rejected,
    NeedsEvidence,
    NeedsAuthority,
    NeedsContract,
    NeedsIdentity,
    NeedsPolicy,
    Defer,
    Quarantine,
    Escalate,
    Rollback,
    Supersede,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ReconciliationRecord {
    pub id: FabricId,
    pub target: FabricId,
    pub desired_state: FabricId,
    pub observed_state: FabricId,
    pub current_state: FabricId,
    pub decision: ReconciliationDecision,
    pub reason: String,
    pub risk: RiskLevel,
    pub validator_result: FabricId,
    pub authority_chain: FabricId,
    pub applied_changes: Vec<FabricId>,
    pub resulting_state: FabricId,
    pub trace: FabricId,
    pub status: LifecycleStatus,
    pub temporal: TemporalContext,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct State {
    pub id: FabricId,
    pub subject: FabricId,
    pub version: u64,
    pub health: String,
    pub relationships: Vec<FabricId>,
    pub derived_from: Vec<FabricId>,
    pub status: LifecycleStatus,
    pub temporal: TemporalContext,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ValidationResult {
    pub id: FabricId,
    pub target: FabricId,
    pub valid: bool,
    pub severity: String,
    pub errors: Vec<String>,
    pub warnings: Vec<String>,
    pub checked_at: DateTime<Utc>,
}

#[derive(Debug, thiserror::Error)]
pub enum FabricError {
    #[error("record not found: {0}")]
    NotFound(FabricId),

    #[error("validation failed: {0}")]
    ValidationFailed(String),

    #[error("authority denied: {0}")]
    AuthorityDenied(String),

    #[error("reconciliation failed: {0}")]
    ReconciliationFailed(String),
}

pub type FabricResult<T> = Result<T, FabricError>;
