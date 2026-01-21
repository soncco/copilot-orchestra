-- =====================================================
-- TravesIA Database - Drop All Objects
-- =====================================================
-- Description: Drops all tables, types, and functions for clean reset
-- Author: Database Agent
-- Date: 2026-01-20
-- Version: 1.0
-- WARNING: This will destroy ALL data!
-- =====================================================
-- Drop all tables in reverse order of dependencies
DROP TABLE IF EXISTS audit_log CASCADE;
DROP TABLE IF EXISTS user_sessions CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS bank_deposits CASCADE;
DROP TABLE IF EXISTS invoices CASCADE;
DROP TABLE IF EXISTS commissions CASCADE;
DROP TABLE IF EXISTS additional_sales CASCADE;
DROP TABLE IF EXISTS group_costs CASCADE;
DROP TABLE IF EXISTS staff_assignments CASCADE;
DROP TABLE IF EXISTS staff CASCADE;
DROP TABLE IF EXISTS special_services CASCADE;
DROP TABLE IF EXISTS accommodations CASCADE;
DROP TABLE IF EXISTS transportation CASCADE;
DROP TABLE IF EXISTS hotels CASCADE;
DROP TABLE IF EXISTS exchange_rates CASCADE;
DROP TABLE IF EXISTS price_periods CASCADE;
DROP TABLE IF EXISTS supplier_services CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS flights CASCADE;
DROP TABLE IF EXISTS itineraries CASCADE;
DROP TABLE IF EXISTS passengers CASCADE;
DROP TABLE IF EXISTS groups CASCADE;
DROP TABLE IF EXISTS programs CASCADE;
-- Drop custom types
DROP TYPE IF EXISTS audit_action CASCADE;
DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS document_category CASCADE;
DROP TYPE IF EXISTS commission_type CASCADE;
DROP TYPE IF EXISTS payment_method CASCADE;
DROP TYPE IF EXISTS invoice_status CASCADE;
DROP TYPE IF EXISTS cost_category CASCADE;
DROP TYPE IF EXISTS staff_role CASCADE;
DROP TYPE IF EXISTS special_service_type CASCADE;
DROP TYPE IF EXISTS accommodation_status CASCADE;
DROP TYPE IF EXISTS transportation_type CASCADE;
DROP TYPE IF EXISTS currency CASCADE;
DROP TYPE IF EXISTS supplier_type CASCADE;
DROP TYPE IF EXISTS group_status CASCADE;
DROP TYPE IF EXISTS group_type CASCADE;
-- Drop functions
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;
-- Note: Extensions are not dropped as they might be used by other databases
-- If you need to drop extensions, run:
-- DROP EXTENSION IF EXISTS "uuid-ossp" CASCADE;
-- DROP EXTENSION IF EXISTS unaccent CASCADE;
-- DROP EXTENSION IF EXISTS pg_trgm CASCADE;
-- DROP EXTENSION IF EXISTS pgcrypto CASCADE;
-- DROP EXTENSION IF EXISTS btree_gist CASCADE;
SELECT 'All TravesIA objects have been dropped successfully.' AS status;