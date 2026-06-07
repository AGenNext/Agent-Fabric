use chrono::{DateTime, Utc};
use fabric_core::{AuthorityChain, FabricId, LifecycleStatus, RiskLevel, TemporalContext};
use fabric_validate::ValidationReport;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum AuthorityDecision {
    Permit,
    Deny,
    Escalate,
    RequireEvidence,
    RequireAuthority,
    Expired,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum AuthorityScope {
    Federation(FabricId),
    Domain(FabricId),
    Cluster(FabricId),
    Box(FabricId),
    Participant(FabricId),
    Record(FabricId),
    Global,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AuthorityAction {
    pub name: String,
}

impl AuthorityAction {
    pub fn new(name: impl Into<String>) -> Self {
        Self { name: name.into() }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AuthorityGrant {
    pub id: FabricId,
    pub authority: FabricId,
    pub subject: FabricId,
    pub action: AuthorityAction,
    pub resource: FabricId,
    pub scope: AuthorityScope,
    pub max_risk: RiskLevel,
    pub status: LifecycleStatus,
    pub temporal: TemporalContext,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AuthorityDelegation {
    pub id: FabricId,
    pub from: FabricId,
    pub to: FabricId,
    pub scope: AuthorityScope,
    pub max_risk: RiskLevel,
    pub status: LifecycleStatus,
    pub temporal: TemporalContext,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AuthorityRequest {
    pub id: FabricId,
    pub actor: FabricId,
    pub action: AuthorityAction,
    pub resource: FabricId,
    pub scope: AuthorityScope,
    pub risk: RiskLevel,
    pub validation: Option<ValidationReport>,
    pub authority_chain: Option<AuthorityChain>,
    pub requested_at: DateTime<Utc>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AuthorityResult {
    pub id: FabricId,
    pub request: FabricId,
    pub decision: AuthorityDecision,
    pub reason: String,
    pub decided_by: FabricId,
    pub decided_at: DateTime<Utc>,
}

pub trait AuthorityEngine {
    fn decide(&self, request: &AuthorityRequest) -> AuthorityResult;
}

pub trait AuthorityResolver {
    fn grants_for(&self, actor: &FabricId) -> Vec<AuthorityGrant>;
}

pub trait DelegationResolver {
    fn delegations_for(&self, actor: &FabricId) -> Vec<AuthorityDelegation>;
}

pub trait ScopeResolver {
    fn scope_contains(&self, parent: &AuthorityScope, child: &AuthorityScope) -> bool;
}

pub trait RiskEvaluator {
    fn allows(&self, grant_risk: &RiskLevel, requested_risk: &RiskLevel) -> bool;
}

#[derive(Debug, Clone, Default)]
pub struct BasicRiskEvaluator;

impl RiskEvaluator for BasicRiskEvaluator {
    fn allows(&self, grant_risk: &RiskLevel, requested_risk: &RiskLevel) -> bool {
        risk_rank(grant_risk) >= risk_rank(requested_risk)
    }
}

fn risk_rank(risk: &RiskLevel) -> u8 {
    match risk {
        RiskLevel::Low => 1,
        RiskLevel::Medium => 2,
        RiskLevel::High => 3,
        RiskLevel::Critical => 4,
    }
}

#[derive(Debug, Clone)]
pub struct StaticAuthorityEngine {
    pub engine_id: FabricId,
    pub grants: Vec<AuthorityGrant>,
}

impl StaticAuthorityEngine {
    pub fn new(engine_id: impl Into<FabricId>, grants: Vec<AuthorityGrant>) -> Self {
        Self {
            engine_id: engine_id.into(),
            grants,
        }
    }
}

impl AuthorityEngine for StaticAuthorityEngine {
    fn decide(&self, request: &AuthorityRequest) -> AuthorityResult {
        let evaluator = BasicRiskEvaluator;
        let now = Utc::now();

        if let Some(validation) = &request.validation {
            if !validation.valid {
                return AuthorityResult {
                    id: format!("authority-result:{}", request.id),
                    request: request.id.clone(),
                    decision: AuthorityDecision::Deny,
                    reason: "Validation report is not valid.".to_string(),
                    decided_by: self.engine_id.clone(),
                    decided_at: now,
                };
            }
        }

        let matching_grant = self.grants.iter().find(|grant| {
            grant.subject == request.actor
                && grant.resource == request.resource
                && grant.action.name == request.action.name
                && grant.status == LifecycleStatus::Active
                && evaluator.allows(&grant.max_risk, &request.risk)
                && temporal_active(&grant.temporal, now)
        });

        if matching_grant.is_some() {
            AuthorityResult {
                id: format!("authority-result:{}", request.id),
                request: request.id.clone(),
                decision: AuthorityDecision::Permit,
                reason: "Active authority grant matched request.".to_string(),
                decided_by: self.engine_id.clone(),
                decided_at: now,
            }
        } else {
            AuthorityResult {
                id: format!("authority-result:{}", request.id),
                request: request.id.clone(),
                decision: AuthorityDecision::Deny,
                reason: "No active authority grant matched request.".to_string(),
                decided_by: self.engine_id.clone(),
                decided_at: now,
            }
        }
    }
}

fn temporal_active(temporal: &TemporalContext, now: DateTime<Utc>) -> bool {
    if let Some(valid_from) = temporal.valid_from {
        if now < valid_from {
            return false;
        }
    }

    if let Some(valid_to) = temporal.valid_to {
        if now > valid_to {
            return false;
        }
    }

    if let Some(expires_at) = temporal.expires_at {
        if now > expires_at {
            return false;
        }
    }

    true
}
