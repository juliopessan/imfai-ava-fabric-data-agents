# .avanade-core - InventoryScout Agent Framework

This folder contains the complete framework definition for the InventoryScout agent following Avanade™ Core standards.

---

## Structure

```
.avanade-core/
├── agents/
│   └── inventory-scout.md          # Complete agent definition
├── tasks/
│   ├── scan-repo.md                # Command: *scan-repo
│   ├── generate-knowledge-graph.md # Command: *generate-knowledge-graph
│   └── ...                         # Other command definitions
├── checklists/
│   └── inventory-checklist.md      # Validation checklist
├── templates/
│   ├── inventory-map-template.md
│   ├── asset-catalog-template.md
│   └── lineage-map-template.md
├── data/
│   └── inventory-best-practices.md # Best practices guide
├── core-config.yaml                # Agent configuration
└── README.md                       # This file
```

---

## Files

### Agent Definition

- **`agents/inventory-scout.md`**
  - Complete agent definition
  - Persona, capabilities, commands
  - Integration points
  - Technical specifications

### Core Configuration

- **`core-config.yaml`**
  - Project metadata
  - Agent configuration
  - Output paths
  - Dependencies
  - Supported technologies

### Tasks (Commands)

Each command has its own detailed documentation in `tasks/`:

| File | Command | Priority |
|------|---------|----------|
| `scan-repo.md` | `*scan-repo` | MANDATORY |
| `analyze-configs.md` | `*analyze-configs` | MANDATORY |
| `map-dependencies.md` | `*map-dependencies` | MANDATORY |
| `detect-tech-stack.md` | `*detect-tech-stack` | RECOMMENDED |
| `build-lineage.md` | `*build-lineage` | RECOMMENDED |
| `catalog-assets.md` | `*catalog-assets` | RECOMMENDED |
| `generate-knowledge-graph.md` | `*generate-knowledge-graph` | OPTIONAL |
| `export-inventory.md` | `*export-inventory` | RECOMMENDED |

### Checklists

- **`checklists/inventory-checklist.md`**
  - Validation checklist for Gate 1
  - Quality checks
  - Completeness criteria
  - Security verification

### Templates

- **`templates/inventory-map-template.md`** - Template for inventory map
- **`templates/asset-catalog-template.md`** - Template for asset catalog
- **`templates/lineage-map-template.md`** - Template for lineage map

### Best Practices

- **`data/inventory-best-practices.md`**
  - Security best practices
  - Performance optimization
  - Quality assurance
  - Visualization guidelines

---

## Usage

### For Users

You don't need to interact with this folder directly. Use the agent via:

```
@inventory-scout
```

### For Developers

If extending or customizing the agent:

1. Edit `core-config.yaml` to change configuration
2. Add new commands in `tasks/`
3. Update `agents/inventory-scout.md` for new capabilities
4. Add templates in `templates/` for new artifact types

---

## Integration

This framework follows **Avanade™ Core for Data Engineering** standards, ensuring compatibility with:

- DataStrategist (Alex)
- BusinessAnalyst (Mary)
- DataArchitect (Winston)
- DataSteward (Gaia)
- Orchestrator (Orion)

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-12
