# Partnership Model

Agent-Fabric distinguishes between vendors, providers, and partners.

A vendor sells a product or service.
A provider supplies a governed capability into the Fabric.
A partner co-delivers outcomes with shared commitments, trust, evidence, and accountability.

## Definition

The Partnership Model defines how external and internal organizations participate in Agent-Fabric service delivery as vendors, providers, delivery partners, technology partners, ecosystem partners, and strategic partners.

```text
Vendor
  -> Provider
  -> Partner
  -> Ecosystem Participant
```

## Core rule

```text
Vendors supply. Providers commit. Partners co-deliver.
```

The Platform Agent remains accountable for the customer-facing service outcome unless the service contract explicitly defines shared accountability.

---

## Roles

## Vendor

A vendor sells a product, tool, model, service, device, infrastructure layer, or support package.

Vendor relationship is commercial first.

```text
Vendor = seller
```

## Provider

A provider supplies a capability into the Fabric under contract, evidence, and commitments.

Provider relationship is operational.

```text
Provider = governed capability supplier
```

## Partner

A partner co-delivers customer outcomes with the Platform Agent.

Partner relationship is strategic and accountable.

```text
Partner = co-delivery participant
```

---

## Partnership tiers

```text
Tier 0: Vendor
Tier 1: Provider
Tier 2: Certified Provider
Tier 3: Delivery Partner
Tier 4: Strategic Partner
Tier 5: Ecosystem Partner
```

## Tier 0: Vendor

Supplies product or service.

Requirements:

```text
commercial agreement
basic identity
product metadata
support contact
```

## Tier 1: Provider

Supplies governed capability.

Requirements:

```text
provider identity
capability declaration
contract
commitments
evidence obligations
risk classification
```

## Tier 2: Certified Provider

Provider validated for Fabric use.

Requirements:

```text
certification evidence
security review
interoperability validation
support commitment
version compatibility
incident process
```

## Tier 3: Delivery Partner

Co-delivers service outcomes.

Requirements:

```text
shared delivery playbook
operator responsibilities
authority boundaries
customer interaction model
SLA/SLO alignment
escalation path
joint evidence reporting
```

## Tier 4: Strategic Partner

Co-develops platform/service capabilities.

Requirements:

```text
roadmap alignment
joint governance
shared reference architecture
joint GTM motion
integration roadmap
executive sponsor
trust framework
```

## Tier 5: Ecosystem Partner

Participates in the broader Fabric ecosystem.

Requirements:

```text
open protocol alignment
certified integrations
marketplace listing
community participation
interoperability commitments
```

---

## Partnership object

Every partner is represented in Fabric.

```json
{
  "id": "partner:canonical",
  "type": "FabricPartner",
  "tier": "strategicPartner",
  "capabilities": ["ubuntu-core", "landscape", "snapcraft"],
  "status": "active"
}
```

---

## Partnership contract

A partnership contract defines:

```text
scope
joint outcome
roles and responsibilities
authority boundaries
commercial model
SLA/SLO
support model
security obligations
compliance obligations
evidence obligations
incident process
termination rules
data handling
customer communication model
```

Rule:

```text
No active partnership without contract, commitments, authority, and evidence obligations.
```

---

## Shared commitments

Partnerships create shared commitments.

Examples:

```text
joint delivery commitment
integration stability commitment
support response commitment
security disclosure commitment
update compatibility commitment
customer escalation commitment
marketplace quality commitment
training/certification commitment
```

---

## Authority boundaries

Partners may receive scoped authority.

Examples:

```text
operate specific Fabric Boxes
support specific customer domain
publish certified participant snap
approve low-risk maintenance
emit compliance evidence
run delivery playbook
```

Partners must not:

```text
approve their own high-risk actions
cross customer boundaries silently
bypass Fabric reconciliation
hide incidents
replace Platform Agent accountability
change customer state outside scope
```

---

## Partnership graph

Canonical relationships:

```text
partner supplies capability
partner coDelivers service
partner boundBy contract
partner authorizedBy authority
partner evidencedBy certification
partner supports domain
partner operates box
partner participatesIn federation
```

Example:

```text
partner:canonical supplies capability:ubuntu-core
capability:ubuntu-core supports service:fabric-box-management
partner:canonical coDelivers service:fabric-box-management
service:fabric-box-management boundBy contract:canonical-agennext
contract:canonical-agennext contains commitment:security-updates
```

---

## Partner lifecycle

```text
proposed
  -> dueDiligence
  -> validating
  -> certified
  -> active
  -> degraded
  -> challenged
  -> suspended
  -> retired
  -> archived
```

Degradation triggers:

```text
SLA breach
security incident
missing evidence
support failure
contract breach
certification expiry
customer escalation
integration failure
```

---

## Service delivery model

```text
Customer Outcome
  -> Platform Agent accountability
  -> Partner capability
  -> Provider commitment
  -> Edge participant execution
  -> Evidence
  -> Reconciled state
  -> Outcome report
```

## One-line definition

Partnership Model turns vendors into governed ecosystem participants: providers commit capabilities, partners co-deliver outcomes, and the Platform Agent remains the accountable service delivery agent through Fabric authority, evidence, and reconciliation.
