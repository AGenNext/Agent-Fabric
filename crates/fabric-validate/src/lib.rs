use chrono::{DateTime, Utc};
use fabric_core::{FabricId, RiskLevel};
use fabric_message::{validate_envelope_shape, Envelope};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum ValidationSeverity {
    Info,
    Warning,
    Error,
    Critical,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ValidationIssue {
    pub code: String,
    pub message: String,
    pub severity: ValidationSeverity,
    pub target: Option<FabricId>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ValidationReport {
    pub id: FabricId,
    pub target: FabricId,
    pub valid: bool,
    pub issues: Vec<ValidationIssue>,
    pub checked_at: DateTime<Utc>,
}

impl ValidationReport {
    pub fn pass(id: impl Into<FabricId>, target: impl Into<FabricId>) -> Self {
        Self {
            id: id.into(),
            target: target.into(),
            valid: true,
            issues: vec![],
            checked_at: Utc::now(),
        }
    }

    pub fn fail(
        id: impl Into<FabricId>,
        target: impl Into<FabricId>,
        issues: Vec<ValidationIssue>,
    ) -> Self {
        Self {
            id: id.into(),
            target: target.into(),
            valid: false,
            issues,
            checked_at: Utc::now(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ValidationContext {
    pub validator: FabricId,
    pub risk: RiskLevel,
    pub authority_chain: Option<FabricId>,
    pub trace: FabricId,
    pub checked_at: DateTime<Utc>,
}

impl ValidationContext {
    pub fn new(validator: FabricId, risk: RiskLevel, trace: FabricId) -> Self {
        Self {
            validator,
            risk,
            authority_chain: None,
            trace,
            checked_at: Utc::now(),
        }
    }
}

pub trait Validator<T> {
    fn validate(&self, target: &T, ctx: &ValidationContext) -> ValidationReport;
}

pub trait EnvelopeValidator: Validator<Envelope> {}

pub trait IdentityValidator<T>: Validator<T> {}

pub trait SchemaValidator<T>: Validator<T> {}

pub trait SemanticValidator<T>: Validator<T> {}

pub trait AuthorityValidator<T>: Validator<T> {}

pub trait TemporalValidator<T>: Validator<T> {}

pub trait RelationshipValidator<T>: Validator<T> {}

pub trait TopologyValidator<T>: Validator<T> {}

pub trait PolicyValidator<T>: Validator<T> {}

pub trait ValidationPipeline<T> {
    fn validate_all(&self, target: &T, ctx: &ValidationContext) -> ValidationReport;
}

#[derive(Debug, Default, Clone)]
pub struct BasicEnvelopeValidator;

impl Validator<Envelope> for BasicEnvelopeValidator {
    fn validate(&self, target: &Envelope, _ctx: &ValidationContext) -> ValidationReport {
        let mut issues = Vec::new();

        if target.id.trim().is_empty() {
            issues.push(ValidationIssue {
                code: "MESSAGE_ID_REQUIRED".to_string(),
                message: "Fabric message id is required.".to_string(),
                severity: ValidationSeverity::Error,
                target: None,
            });
        }

        if target.source.trim().is_empty() {
            issues.push(ValidationIssue {
                code: "SOURCE_REQUIRED".to_string(),
                message: "Fabric message source is required.".to_string(),
                severity: ValidationSeverity::Error,
                target: Some(target.id.clone()),
            });
        }

        if target.subject.trim().is_empty() {
            issues.push(ValidationIssue {
                code: "SUBJECT_REQUIRED".to_string(),
                message: "Fabric message subject is required.".to_string(),
                severity: ValidationSeverity::Error,
                target: Some(target.id.clone()),
            });
        }

        if target.trace.trim().is_empty() {
            issues.push(ValidationIssue {
                code: "TRACE_REQUIRED".to_string(),
                message: "Fabric message trace is required.".to_string(),
                severity: ValidationSeverity::Error,
                target: Some(target.id.clone()),
            });
        }

        if target.intent.trim().is_empty() {
            issues.push(ValidationIssue {
                code: "INTENT_REQUIRED".to_string(),
                message: "Fabric message intent is required.".to_string(),
                severity: ValidationSeverity::Error,
                target: Some(target.id.clone()),
            });
        }

        if target.identity.trim().is_empty() {
            issues.push(ValidationIssue {
                code: "IDENTITY_REQUIRED".to_string(),
                message: "Fabric message identity is required.".to_string(),
                severity: ValidationSeverity::Error,
                target: Some(target.id.clone()),
            });
        }

        if validate_envelope_shape(target).is_err() {
            issues.push(ValidationIssue {
                code: "MESSAGE_TYPE_PAYLOAD_MISMATCH".to_string(),
                message: "Fabric message type must match payload kind.".to_string(),
                severity: ValidationSeverity::Error,
                target: Some(target.id.clone()),
            });
        }

        if issues.is_empty() {
            ValidationReport::pass(format!("validation:{}", target.id), target.id.clone())
        } else {
            ValidationReport::fail(format!("validation:{}", target.id), target.id.clone(), issues)
        }
    }
}

impl EnvelopeValidator for BasicEnvelopeValidator {}
