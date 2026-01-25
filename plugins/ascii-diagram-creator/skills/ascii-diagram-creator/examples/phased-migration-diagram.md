# Example: Phased Migration Diagram

## Scenario

A user asks: "Create a diagram showing our database migration phases with current progress."

## Generated Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│           DATABASE MIGRATION: MONGODB TO POSTGRESQL                      │
│                      Target: Q4 2025 Completion                          │
└─────────────────────────────────────────────────────────────────────────┘

PHASE 1: Schema Design & Setup ✓
┌─────────────────────────────────────────────────────────────────────────┐
│ Status: COMPLETE                                           Duration: 2w │
├─────────────────────────────────────────────────────────────────────────┤
│ ✓ Analyze MongoDB collections and relationships                         │
│ ✓ Design PostgreSQL schema with proper normalization                    │
│ ✓ Create migration scripts and rollback procedures                      │
│ ✓ Set up staging environment with both databases                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
PHASE 2: Dual-Write Implementation ✓
┌─────────────────────────────────────────────────────────────────────────┐
│ Status: COMPLETE                                           Duration: 3w │
├─────────────────────────────────────────────────────────────────────────┤
│ ✓ Implement write-through to both MongoDB and PostgreSQL                │
│ ✓ Add feature flags for gradual rollout                                 │
│ ✓ Deploy to staging and validate data consistency                       │
│ ✓ Monitor for performance impact (< 50ms added latency)                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
PHASE 3: Historical Data Migration ⏳
┌─────────────────────────────────────────────────────────────────────────┐
│ Status: IN PROGRESS (60%)                                  Duration: 4w │
├─────────────────────────────────────────────────────────────────────────┤
│ ✓ Migrate users collection (2.3M records)                               │
│ ✓ Migrate products collection (150K records)                            │
│ ⏳ Migrate orders collection (5.2M records) - 60% complete              │
│   Migrate reviews collection (890K records)                             │
│   Validate data integrity across all tables                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
PHASE 4: Read Path Migration
┌─────────────────────────────────────────────────────────────────────────┐
│ Status: PENDING                                            Duration: 2w │
├─────────────────────────────────────────────────────────────────────────┤
│   Switch read operations to PostgreSQL (feature flag)                   │
│   Run parallel queries and compare results                              │
│   Gradually increase PostgreSQL read traffic (10% → 100%)               │
│   Monitor query performance and optimize indexes                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
PHASE 5: Cutover & Cleanup
┌─────────────────────────────────────────────────────────────────────────┐
│ Status: PENDING                                            Duration: 1w │
├─────────────────────────────────────────────────────────────────────────┤
│   Disable MongoDB writes                                                │
│   Update all application configuration                                  │
│   Archive MongoDB data                                                  │
│   Remove dual-write code and feature flags                              │
│   Document lessons learned                                              │
└─────────────────────────────────────────────────────────────────────────┘

Summary: Phase 3 of 5 │ Overall Progress: ~55% │ On Track for Q4

Legend:
✓ = Complete    ⏳ = In Progress    (blank) = Pending
```

## Explanation

This phased migration diagram provides:

- **Clear progress visibility**: Status and completion percentage per phase
- **Detailed tasks**: Specific actions within each phase
- **Time estimates**: Duration for planning purposes
- **Overall summary**: Quick status check at the bottom

The vertical flow shows dependencies between phases while the detailed boxes provide actionable information.

## Usage Suggestions

- Include in weekly status updates
- Add to project management tools
- Share with stakeholders for progress visibility
- Update after each milestone completion
