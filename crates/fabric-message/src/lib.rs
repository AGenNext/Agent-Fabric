use chrono::{DateTime, Utc};
use fabric_core::{
    AuthorityChain, CommitmentRecord, Event, FabricId, GapFillProposal, ReconciliationRecord,
    RiskLevel, State, Trace, ValidationResult,
};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use uuid::Uuid;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum MessageType {
    Observe,
    Propose,
    Validate,
    Approve,
    Reject,
    Commit,
    Challenge,
    Reconcile,
    Project,
    Query,
    Notify,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Envelope {
    pub id: FabricId,
    pub spec_version: String,
    pub message_type: MessageType,
    pub source: FabricId,
    pub recipient: Option<FabricId>,
    pub subject: FabricId,
    pub time: DateTime<Utc>,
    pub trace: FabricId,
    pub correlation_id: Option<FabricId>,
    pub causation_id: Option<FabricId>,
    pub intent: FabricId,
    pub identity: FabricId,
    pub authority_chain: Option<FabricId>,
    pub risk: RiskLevel,
    pub payload: MessagePayload,
}

impl Envelope {
    pub fn new(
        message_type: MessageType,
        source: FabricId,
        subject: FabricId,
        trace: FabricId,
        intent: FabricId,
        identity: FabricId,
        risk: RiskLevel,
        payload: MessagePayload,
    ) -> Self {
        Self {
            id: format!("msg:{}", Uuid::new_v4()),
            spec_version: "1.0".to_string(),
            message_type,
            source,
            recipient: None,
            subject,
            time: Utc::now(),
            trace,
            correlation_id: None,
            causation_id: None,
            intent,
            identity,
            authority_chain: None,
            risk,
            payload,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "kind", content = "data")]
pub enum MessagePayload {
    Observe(ObservePayload),
    Propose(ProposePayload),
    Validate(ValidatePayload),
    Approve(ApprovePayload),
    Reject(RejectPayload),
    Commit(CommitPayload),
    Challenge(ChallengePayload),
    Reconcile(ReconcilePayload),
    Project(ProjectPayload),
    Query(QueryPayload),
    Notify(NotifyPayload),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ObservePayload {
    pub event: Event,
    pub trace_record: Option<Trace>,
    pub observed_state: Option<State>,
    pub evidence: Vec<FabricId>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum ProposalRecord {
    GapFill(GapFillProposal),
    Generic(Value),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ProposePayload {
    pub proposal: ProposalRecord,
    pub approval_required: bool,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ValidatePayload {
    pub target: FabricId,
    pub result: ValidationResult,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ApprovePayload {
    pub target: FabricId,
    pub authority_chain: AuthorityChain,
    pub scope: String,
    pub expires_at: Option<DateTime<Utc>>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct RejectPayload {
    pub target: FabricId,
    pub reason: String,
    pub authority_chain: Option<FabricId>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct CommitPayload {
    pub commitment: CommitmentRecord,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ChallengePayload {
    pub target: FabricId,
    pub reason: String,
    pub requested_action: String,
    pub evidence: Vec<FabricId>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ReconcilePayload {
    pub target: FabricId,
    pub desired_state: FabricId,
    pub observed_state: FabricId,
    pub reconciliation_record: Option<ReconciliationRecord>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ProjectPayload {
    pub projection_contract: FabricId,
    pub state: State,
    pub derived_from: Vec<FabricId>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum QueryType {
    StateAsOf,
    RelationshipsFor,
    CommitmentsFor,
    AuthorityFor,
    EvidenceFor,
    TraceFor,
    OpenProposals,
    ActiveDrift,
    ReachableFrom,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct QueryPayload {
    pub query_type: QueryType,
    pub target: FabricId,
    pub as_of: Option<DateTime<Utc>>,
    pub parameters: Value,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct NotifyPayload {
    pub notification_type: String,
    pub target: FabricId,
    pub state: Option<FabricId>,
    pub details: Value,
}

#[derive(Debug, thiserror::Error)]
pub enum MessageError {
    #[error("message type and payload kind do not match")]
    TypePayloadMismatch,
}

pub fn validate_envelope_shape(envelope: &Envelope) -> Result<(), MessageError> {
    let matches = matches!(
        (&envelope.message_type, &envelope.payload),
        (MessageType::Observe, MessagePayload::Observe(_))
            | (MessageType::Propose, MessagePayload::Propose(_))
            | (MessageType::Validate, MessagePayload::Validate(_))
            | (MessageType::Approve, MessagePayload::Approve(_))
            | (MessageType::Reject, MessagePayload::Reject(_))
            | (MessageType::Commit, MessagePayload::Commit(_))
            | (MessageType::Challenge, MessagePayload::Challenge(_))
            | (MessageType::Reconcile, MessagePayload::Reconcile(_))
            | (MessageType::Project, MessagePayload::Project(_))
            | (MessageType::Query, MessagePayload::Query(_))
            | (MessageType::Notify, MessagePayload::Notify(_))
    );

    if matches {
        Ok(())
    } else {
        Err(MessageError::TypePayloadMismatch)
    }
}
