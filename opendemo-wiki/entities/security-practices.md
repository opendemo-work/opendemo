---
title: Security Practices
category: entities
tags: [security, encryption, compliance, cloud]
sources: [/Users/allengaller/Documents/GitHub/opendemo-work/opendemo/README.md, /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/DETAILED_STRUCTURE.md]
summary: Security practices covering full disk encryption (LUKS, BitLocker, FileVault), TPM 2.0, HSM, key management (Vault, AWS/Azure/GCP KMS), cloud security, and compliance frameworks (GDPR, HIPAA, PCI-DSS, SOC2).
provenance:
  extracted: 0.85
  inferred: 0.15
  ambiguous: 0.0
base_confidence: 0.7
lifecycle: draft
lifecycle_changed: 2026-06-03
tier: supporting
created: 2026-06-03T05:33:46Z
updated: 2026-06-03T05:33:46Z
---

# Security Practices

Security practices in OpenDemo cover enterprise-grade security implementations across cloud and on-premises environments.

## Case Catalog

### Full Disk Encryption (FDE)
| Case | Description |
|------|-------------|
| fde-luks | Linux full disk encryption with LUKS |
| fde-tpm-unified | TPM + PIN unified security architecture |
| cloud-fde-aws | AWS cloud instance FDE |
| luks-remote-unlock | LUKS remote unlock |
| disk-encryption-opal | OPAL self-encrypting drives |
| bitlocker-management | Windows BitLocker |
| filevault-management | macOS FileVault |

### Trusted Computing
| Case | Description |
|------|-------------|
| tpm-security | TPM 2.0 security module |
| secure-boot | UEFI secure boot |
| hsm-basics | Hardware Security Module basics |

### Key Management
| Case | Description |
|------|-------------|
| secrets-management-vault | HashiCorp Vault secrets |
| crypto-key-management | Key lifecycle management |

### Cloud Security
AWS, Azure, and GCP cloud security implementations with BYOK/HYOK support.

### Compliance
| Framework | Coverage |
|-----------|----------|
| GDPR | EU data protection |
| HIPAA | US healthcare data |
| PCI-DSS | Payment card data |
| SOC2 | Service organization controls |

## Technology Integration

Security practices integrate with [[entities/tech-stacks]] particularly:
- [[entities/sre-practices]] — For operational security
- [[entities/tech-stacks]] — For Kubernetes security (80 cases)

## Related

- [[entities/tech-stacks]] — All technology stacks
- [[references/opendemo-project]] — Project overview
