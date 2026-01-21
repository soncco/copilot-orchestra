/**
 * TypeScript types for TravesIA
 */

// User & Authentication
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone: string;
  role: 'admin' | 'manager' | 'sales' | 'guide' | 'operations';
  is_admin: boolean;
  is_manager: boolean;
  is_sales: boolean;
  is_guide: boolean;
  is_operations: boolean;
  is_active: boolean;
  mfa_enabled: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
  mfa_code?: string;
}

export interface LoginResponse {
  user: User;
  tokens: {
    access: string;
    refresh: string;
  };
  requires_mfa?: boolean;
}

export interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  phone?: string;
}

// Programs & Circuits
export interface Program {
  id: string;
  code: string;
  name: string;
  description: string;
  destination: string;
  duration_days: number;
  duration_nights: number;
  price_per_person: number;
  currency: string;
  min_participants: number;
  max_participants: number;
  difficulty_level: 'easy' | 'moderate' | 'challenging' | 'extreme';
  season_best: string;
  includes: string[];
  excludes: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Group {
  id: string;
  code: string;
  program: string;
  program_name?: string;
  start_date: string;
  end_date: string;
  status: 'planning' | 'confirmed' | 'in_progress' | 'completed' | 'cancelled';
  total_passengers: number;
  guide: string | null;
  guide_name?: string;
  budget: number;
  actual_cost: number;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface Passenger {
  id: string;
  group: string;
  group_code?: string;
  first_name: string;
  last_name: string;
  full_name?: string;
  email: string;
  phone: string;
  document_type: 'dni' | 'passport' | 'ce' | 'other';
  document_number: string;
  nationality: string;
  date_of_birth: string;
  gender: 'M' | 'F' | 'O';
  emergency_contact_name: string;
  emergency_contact_phone: string;
  dietary_restrictions: string;
  medical_conditions: string;
  status: 'pending' | 'confirmed' | 'paid' | 'cancelled';
  payment_status: 'pending' | 'partial' | 'paid' | 'refunded';
  total_paid: number;
  balance_due: number;
  created_at: string;
  updated_at: string;
}

// Suppliers
export interface Supplier {
  id: string;
  code: string;
  name: string;
  supplier_type:
    | 'hotel'
    | 'restaurant'
    | 'transport'
    | 'guide'
    | 'attraction'
    | 'insurance'
    | 'other';
  status: 'active' | 'inactive' | 'suspended';
  contact_name: string;
  contact_email: string;
  contact_phone: string;
  address: string;
  city: string;
  country: string;
  tax_id: string;
  payment_terms: string;
  bank_account: string;
  rating: number;
  notes: string;
  created_at: string;
  updated_at: string;
}

// Operations
export interface Hotel {
  id: string;
  group: string;
  group_code?: string;
  supplier: string;
  supplier_name?: string;
  hotel_name: string;
  city: string;
  address: string;
  check_in: string;
  check_out: string;
  nights: number;
  room_type: string;
  number_of_rooms: number;
  booking_reference: string;
  status: 'pending' | 'confirmed' | 'cancelled';
  price_per_night: number;
  total_price: number;
  includes_breakfast: boolean;
  created_at: string;
  updated_at: string;
}

export interface Staff {
  id: string;
  first_name: string;
  last_name: string;
  full_name?: string;
  staff_type: 'guide' | 'driver' | 'coordinator';
  status: 'active' | 'inactive';
  email: string;
  phone: string;
  address: string;
  city: string;
  languages: string[];
  certifications: string;
  license_number: string;
  rate_per_day: number;
  currency: string;
  rating: number;
  created_at: string;
  updated_at: string;
}

// Financial
export interface Invoice {
  id: string;
  passenger: string;
  passenger_name?: string;
  invoice_type: 'boleta' | 'factura' | 'nota_credito' | 'nota_debito';
  invoice_number: string;
  issue_date: string;
  due_date: string | null;
  status: 'draft' | 'issued' | 'sent' | 'accepted' | 'rejected' | 'cancelled';
  customer_name: string;
  customer_document_type: string;
  customer_document_number: string;
  subtotal: number;
  tax_amount: number;
  total_amount: number;
  currency: string;
  paid: boolean;
  payment_date: string | null;
  payment_method: string;
  created_at: string;
  updated_at: string;
}

// Documents
export interface Document {
  id: string;
  name: string;
  description: string;
  document_type:
    | 'contract'
    | 'invoice'
    | 'receipt'
    | 'passport'
    | 'visa'
    | 'insurance'
    | 'itinerary'
    | 'voucher'
    | 'ticket'
    | 'photo'
    | 'report'
    | 'other';
  file: string;
  file_url: string;
  file_size: number;
  mime_type: string;
  related_to: 'group' | 'passenger' | 'supplier' | 'general';
  group: string | null;
  group_code?: string;
  passenger: string | null;
  passenger_name?: string;
  supplier: string | null;
  supplier_name?: string;
  uploaded_by: string;
  uploaded_by_name?: string;
  tags: string[];
  is_public: boolean;
  is_archived: boolean;
  expires_at: string | null;
  is_expired: boolean;
  notes: string;
  created_at: string;
  updated_at: string;
}

// API Response types
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ErrorResponse {
  detail?: string;
  message?: string;
  errors?: Record<string, string[]>;
}
