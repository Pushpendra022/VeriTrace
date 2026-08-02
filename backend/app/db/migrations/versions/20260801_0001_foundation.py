"""Create VeriTrace persistence tables."""

import sqlalchemy as sa
from alembic import op

revision = "20260801_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("documents", sa.Column("id", sa.String(36), primary_key=True), sa.Column("filename", sa.String(255), nullable=False), sa.Column("original_filename", sa.String(255), nullable=False), sa.Column("mime_type", sa.String(100), nullable=False), sa.Column("file_size", sa.BigInteger(), nullable=False), sa.Column("status", sa.String(30), nullable=False), sa.Column("page_count", sa.Integer(), nullable=False), sa.Column("character_count", sa.Integer(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_documents_status", "documents", ["status"])
    op.create_table("document_pages", sa.Column("id", sa.String(36), primary_key=True), sa.Column("document_id", sa.String(36), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False), sa.Column("page_number", sa.Integer(), nullable=False), sa.Column("text", sa.Text(), nullable=False), sa.Column("start_char", sa.Integer(), nullable=False), sa.Column("end_char", sa.Integer(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_document_pages_document_id", "document_pages", ["document_id"])
    op.create_table("document_chunks", sa.Column("id", sa.String(36), primary_key=True), sa.Column("document_id", sa.String(36), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False), sa.Column("page_number", sa.Integer(), nullable=False), sa.Column("text", sa.Text(), nullable=False), sa.Column("start_char", sa.Integer(), nullable=False), sa.Column("end_char", sa.Integer(), nullable=False), sa.Column("token_estimate", sa.Integer(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_document_chunks_document_id", "document_chunks", ["document_id"])
    op.create_table("claims", sa.Column("id", sa.String(36), primary_key=True), sa.Column("document_id", sa.String(36), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False), sa.Column("claim_text", sa.Text(), nullable=False), sa.Column("category", sa.String(50), nullable=False), sa.Column("importance", sa.String(20), nullable=False), sa.Column("source_type", sa.String(20), nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_claims_document_id", "claims", ["document_id"])
    op.create_table("verifications", sa.Column("id", sa.String(36), primary_key=True), sa.Column("claim_id", sa.String(36), sa.ForeignKey("claims.id", ondelete="CASCADE"), nullable=False), sa.Column("verdict", sa.String(20), nullable=False), sa.Column("confidence", sa.Float(), nullable=False), sa.Column("quote", sa.Text(), nullable=False), sa.Column("explanation", sa.Text(), nullable=False), sa.Column("page_number", sa.Integer()), sa.Column("chunk_id", sa.String(36), sa.ForeignKey("document_chunks.id", ondelete="SET NULL")), sa.Column("start_char", sa.Integer()), sa.Column("end_char", sa.Integer()), sa.Column("quote_verified", sa.Boolean(), nullable=False), sa.Column("numbers_consistent", sa.Boolean(), nullable=False), sa.Column("percentages_consistent", sa.Boolean(), nullable=False), sa.Column("dates_consistent", sa.Boolean(), nullable=False), sa.Column("currency_consistent", sa.Boolean(), nullable=False), sa.Column("latency_ms", sa.Integer(), nullable=False), sa.Column("chunks_searched", sa.Integer(), nullable=False), sa.Column("chunks_retrieved", sa.Integer(), nullable=False), sa.Column("context_characters", sa.Integer(), nullable=False), sa.Column("provider", sa.String(30), nullable=False), sa.Column("model", sa.String(100), nullable=False), sa.Column("prompt_version", sa.String(30), nullable=False), sa.Column("raw_model_response", sa.Text(), nullable=False), sa.Column("claim_fingerprint", sa.String(64), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_verifications_claim_id", "verifications", ["claim_id"]); op.create_index("ix_verifications_verdict", "verifications", ["verdict"]); op.create_index("ix_verifications_claim_fingerprint", "verifications", ["claim_fingerprint"])


def downgrade() -> None:
    op.drop_table("verifications"); op.drop_table("claims"); op.drop_table("document_chunks"); op.drop_table("document_pages"); op.drop_table("documents")
