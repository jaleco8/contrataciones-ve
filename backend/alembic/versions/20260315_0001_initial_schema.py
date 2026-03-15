"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-03-15

Crea el esquema completo de la Plataforma Abierta Anticorrupción Venezuela:
- Tablas: suppliers, processes, contracts, contract_amendments,
          contract_payments, risk_alerts
- Extensiones: uuid-ossp, pg_trgm
- Índices (incluyendo GIN para búsqueda de texto)
- Trigger update_updated_at para todas las tablas principales
- Vistas: v_buyer_summary, v_supplier_concentration, v_dashboard_stats
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

# revision identifiers
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


# ---------------------------------------------------------------------------
# UPGRADE
# ---------------------------------------------------------------------------

def upgrade() -> None:
    # ------------------------------------------------------------------
    # Extensions
    # ------------------------------------------------------------------
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute('CREATE EXTENSION IF NOT EXISTS "pg_trgm"')

    # ------------------------------------------------------------------
    # TABLE: suppliers
    # ------------------------------------------------------------------
    op.create_table(
        "suppliers",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("rif", sa.String(20), unique=True, nullable=False),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("legal_name", sa.String(500)),
        sa.Column("sector", sa.String(200)),
        sa.Column("type", sa.String(50), server_default="company"),
        sa.Column("sanction_status", sa.String(50), server_default="active"),
        sa.Column("awards_count_12m", sa.Integer(), server_default="0"),
        sa.Column("total_awarded_12m", sa.Numeric(20, 2), server_default="0.00"),
        sa.Column("address", sa.Text()),
        sa.Column("state", sa.String(100)),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_suppliers_rif", "suppliers", ["rif"])
    op.create_index("idx_suppliers_sanction", "suppliers", ["sanction_status"])
    op.create_index("idx_suppliers_sector", "suppliers", ["sector"])
    op.execute(
        "CREATE INDEX idx_suppliers_name_trgm ON suppliers "
        "USING GIN (name gin_trgm_ops)"
    )

    # ------------------------------------------------------------------
    # TABLE: processes
    # ------------------------------------------------------------------
    op.create_table(
        "processes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("ocid", sa.String(100), unique=True),
        sa.Column("title", sa.String(1000), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("status", sa.String(50), nullable=False, server_default="planned"),
        sa.Column("procurement_method", sa.String(100)),
        sa.Column("buyer_name", sa.String(500), nullable=False),
        sa.Column("buyer_id", sa.String(100)),
        sa.Column("buyer_entity_type", sa.String(100)),
        sa.Column("tender_amount", sa.Numeric(20, 2)),
        sa.Column("tender_currency", sa.String(10), server_default="USD"),
        sa.Column("awarded_amount", sa.Numeric(20, 2)),
        sa.Column("awarded_currency", sa.String(10), server_default="USD"),
        sa.Column(
            "awarded_supplier_id", UUID(as_uuid=True),
            sa.ForeignKey("suppliers.id", name="fk_processes_supplier"),
        ),
        sa.Column("awarded_supplier_name", sa.String(500)),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("tender_start_date", sa.Date()),
        sa.Column("tender_end_date", sa.Date()),
        sa.Column("award_date", sa.Date()),
        sa.Column("category", sa.String(200)),
        sa.Column("cpv_code", sa.String(50)),
        sa.Column("bidders_count", sa.Integer(), server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_processes_ocid", "processes", ["ocid"])
    op.create_index("idx_processes_status", "processes", ["status"])
    op.create_index("idx_processes_buyer", "processes", ["buyer_name"])
    op.create_index("idx_processes_awarded_supplier", "processes", ["awarded_supplier_id"])
    op.create_index("idx_processes_category", "processes", ["category"])
    op.create_index("idx_processes_published", "processes",
                    ["published_at"], postgresql_ops={"published_at": "DESC"})
    op.execute(
        "CREATE INDEX idx_processes_title_trgm ON processes "
        "USING GIN (title gin_trgm_ops)"
    )

    # ------------------------------------------------------------------
    # TABLE: contracts
    # ------------------------------------------------------------------
    op.create_table(
        "contracts",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("contract_number", sa.String(200), unique=True, nullable=False),
        sa.Column(
            "process_id", UUID(as_uuid=True),
            sa.ForeignKey("processes.id", name="fk_contracts_process"),
        ),
        sa.Column(
            "supplier_id", UUID(as_uuid=True),
            sa.ForeignKey("suppliers.id", name="fk_contracts_supplier"),
        ),
        sa.Column("supplier_name", sa.String(500), nullable=False),
        sa.Column("buyer_name", sa.String(500), nullable=False),
        sa.Column("buyer_id", sa.String(100)),
        sa.Column("title", sa.String(1000), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("category", sa.String(200)),
        sa.Column("status", sa.String(50), nullable=False, server_default="draft"),
        sa.Column("amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("currency", sa.String(10), server_default="USD"),
        sa.Column("original_amount", sa.Numeric(20, 2)),
        sa.Column("signed_at", sa.Date()),
        sa.Column("start_date", sa.Date()),
        sa.Column("end_date", sa.Date()),
        sa.Column("has_amendments", sa.Boolean(), server_default="false"),
        sa.Column("amendments_count", sa.Integer(), server_default="0"),
        sa.Column("amendment_amount_increase", sa.Numeric(20, 2), server_default="0.00"),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.text("NOW()"), nullable=False),
        sa.Column("status_changed_at", sa.DateTime(timezone=True)),
    )
    op.create_index("idx_contracts_number", "contracts", ["contract_number"])
    op.create_index("idx_contracts_process", "contracts", ["process_id"])
    op.create_index("idx_contracts_supplier", "contracts", ["supplier_id"])
    op.create_index("idx_contracts_buyer", "contracts", ["buyer_name"])
    op.create_index("idx_contracts_status", "contracts", ["status"])
    op.create_index("idx_contracts_signed", "contracts",
                    ["signed_at"], postgresql_ops={"signed_at": "DESC"})
    op.create_index("idx_contracts_amount", "contracts",
                    ["amount"], postgresql_ops={"amount": "DESC"})
    op.execute(
        "CREATE INDEX idx_contracts_title_trgm ON contracts "
        "USING GIN (title gin_trgm_ops)"
    )

    # ------------------------------------------------------------------
    # TABLE: contract_amendments
    # ------------------------------------------------------------------
    op.create_table(
        "contract_amendments",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column(
            "contract_id", UUID(as_uuid=True),
            sa.ForeignKey("contracts.id", ondelete="CASCADE",
                          name="fk_amendments_contract"),
            nullable=False,
        ),
        sa.Column("amendment_number", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("original_amount", sa.Numeric(20, 2)),
        sa.Column("new_amount", sa.Numeric(20, 2)),
        sa.Column("amount_change", sa.Numeric(20, 2)),
        sa.Column("original_end_date", sa.Date()),
        sa.Column("new_end_date", sa.Date()),
        sa.Column("signed_at", sa.Date()),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_amendments_contract", "contract_amendments", ["contract_id"])

    # ------------------------------------------------------------------
    # TABLE: contract_payments
    # ------------------------------------------------------------------
    op.create_table(
        "contract_payments",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column(
            "contract_id", UUID(as_uuid=True),
            sa.ForeignKey("contracts.id", ondelete="CASCADE",
                          name="fk_payments_contract"),
            nullable=False,
        ),
        sa.Column("payment_number", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("currency", sa.String(10), server_default="USD"),
        sa.Column("status", sa.String(50), server_default="paid"),
        sa.Column("payment_date", sa.Date()),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_payments_contract", "contract_payments", ["contract_id"])

    # ------------------------------------------------------------------
    # TABLE: risk_alerts
    # ------------------------------------------------------------------
    op.create_table(
        "risk_alerts",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("type", sa.String(100), nullable=False),
        sa.Column("severity", sa.String(20), nullable=False, server_default="medium"),
        sa.Column("status", sa.String(50), nullable=False, server_default="open"),
        sa.Column("score", sa.Numeric(4, 3), nullable=False, server_default="0.500"),
        sa.Column(
            "contract_id", UUID(as_uuid=True),
            sa.ForeignKey("contracts.id", name="fk_alerts_contract"),
        ),
        sa.Column(
            "process_id", UUID(as_uuid=True),
            sa.ForeignKey("processes.id", name="fk_alerts_process"),
        ),
        sa.Column(
            "supplier_id", UUID(as_uuid=True),
            sa.ForeignKey("suppliers.id", name="fk_alerts_supplier"),
        ),
        sa.Column("explanation", JSONB(), nullable=False,
                  server_default=sa.text("'[]'::jsonb")),
        sa.Column("supporting_data", JSONB(),
                  server_default=sa.text("'{}'::jsonb")),
        sa.Column("reviewed_by", sa.String(200)),
        sa.Column("reviewed_at", sa.DateTime(timezone=True)),
        sa.Column("review_notes", sa.Text()),
        sa.Column("generated_at", sa.DateTime(timezone=True),
                  server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_alerts_type", "risk_alerts", ["type"])
    op.create_index("idx_alerts_severity", "risk_alerts", ["severity"])
    op.create_index("idx_alerts_status", "risk_alerts", ["status"])
    op.create_index("idx_alerts_contract", "risk_alerts", ["contract_id"])
    op.create_index("idx_alerts_supplier", "risk_alerts", ["supplier_id"])
    op.create_index("idx_alerts_generated", "risk_alerts",
                    ["generated_at"], postgresql_ops={"generated_at": "DESC"})
    op.create_index("idx_alerts_score", "risk_alerts",
                    ["score"], postgresql_ops={"score": "DESC"})

    # ------------------------------------------------------------------
    # TRIGGER FUNCTION: update_updated_at_column
    # ------------------------------------------------------------------
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql'
    """)

    for table in ("suppliers", "processes", "contracts", "risk_alerts"):
        op.execute(f"""
            CREATE TRIGGER update_{table}_updated_at
                BEFORE UPDATE ON {table}
                FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()
        """)

    # ------------------------------------------------------------------
    # VIEWS
    # ------------------------------------------------------------------
    op.execute("""
        CREATE OR REPLACE VIEW v_buyer_summary AS
        SELECT
            buyer_name,
            COUNT(*) AS contracts_count,
            SUM(amount) AS total_amount,
            AVG(amount) AS avg_amount,
            COUNT(CASE WHEN has_amendments THEN 1 END) AS amended_count
        FROM contracts
        WHERE status != 'cancelled'
        GROUP BY buyer_name
        ORDER BY total_amount DESC
    """)

    op.execute("""
        CREATE OR REPLACE VIEW v_supplier_concentration AS
        SELECT
            s.id,
            s.rif,
            s.name,
            s.sanction_status,
            COUNT(c.id) AS contracts_count,
            SUM(c.amount) AS total_amount,
            COUNT(DISTINCT c.buyer_name) AS unique_buyers,
            COUNT(ra.id) AS alerts_count
        FROM suppliers s
        LEFT JOIN contracts c
            ON c.supplier_id = s.id AND c.status != 'cancelled'
        LEFT JOIN risk_alerts ra
            ON ra.supplier_id = s.id AND ra.status = 'open'
        GROUP BY s.id, s.rif, s.name, s.sanction_status
        ORDER BY total_amount DESC
    """)

    op.execute("""
        CREATE OR REPLACE VIEW v_dashboard_stats AS
        SELECT
            (SELECT COUNT(*) FROM contracts WHERE status = 'active')
                AS active_contracts,
            (SELECT COUNT(*) FROM contracts)
                AS total_contracts,
            (SELECT COALESCE(SUM(amount), 0) FROM contracts WHERE status != 'cancelled')
                AS total_value_usd,
            (SELECT COUNT(*) FROM suppliers WHERE sanction_status = 'active')
                AS active_suppliers,
            (SELECT COUNT(*) FROM risk_alerts WHERE status = 'open')
                AS open_alerts,
            (SELECT COUNT(*) FROM risk_alerts
             WHERE severity IN ('high', 'critical') AND status = 'open')
                AS critical_alerts,
            (SELECT COUNT(*) FROM processes WHERE status = 'tender')
                AS active_tenders,
            (SELECT COUNT(*) FROM contracts WHERE has_amendments = TRUE)
                AS amended_contracts
    """)


# ---------------------------------------------------------------------------
# DOWNGRADE
# ---------------------------------------------------------------------------

def downgrade() -> None:
    # Views
    op.execute("DROP VIEW IF EXISTS v_dashboard_stats")
    op.execute("DROP VIEW IF EXISTS v_supplier_concentration")
    op.execute("DROP VIEW IF EXISTS v_buyer_summary")

    # Triggers
    for table in ("suppliers", "processes", "contracts", "risk_alerts"):
        op.execute(f"DROP TRIGGER IF EXISTS update_{table}_updated_at ON {table}")

    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")

    # Tables (reverse FK order)
    op.drop_table("risk_alerts")
    op.drop_table("contract_payments")
    op.drop_table("contract_amendments")
    op.drop_table("contracts")
    op.drop_table("processes")
    op.drop_table("suppliers")
