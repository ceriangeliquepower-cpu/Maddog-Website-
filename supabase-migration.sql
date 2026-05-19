-- ─────────────────────────────────────────────────────────────────────────────
-- Maddog Performance Institute — Supabase schema migration
-- Run this entire script once in the Supabase SQL Editor:
--   Dashboard → SQL Editor → New query → paste → Run
-- Safe to run more than once (all changes are guarded with IF NOT EXISTS).
-- ─────────────────────────────────────────────────────────────────────────────


-- ══════════════════════════════════════════════════════════════════════════════
-- 1. SERVICES  (table already exists — add missing columns only)
-- ══════════════════════════════════════════════════════════════════════════════

ALTER TABLE services
  ADD COLUMN IF NOT EXISTS "group"        text,
  ADD COLUMN IF NOT EXISTS color          text,
  ADD COLUMN IF NOT EXISTS billing        text    DEFAULT 'session',
  ADD COLUMN IF NOT EXISTS allow_trial    boolean DEFAULT false,
  ADD COLUMN IF NOT EXISTS enquiry        boolean DEFAULT false,
  ADD COLUMN IF NOT EXISTS desc           text,
  ADD COLUMN IF NOT EXISTS capacity       integer,
  ADD COLUMN IF NOT EXISTS display_order  integer DEFAULT 0;

-- Constrain billing to allowed values
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'services_billing_check'
  ) THEN
    ALTER TABLE services
      ADD CONSTRAINT services_billing_check
        CHECK (billing IN ('session', 'monthly'));
  END IF;
END$$;


-- ══════════════════════════════════════════════════════════════════════════════
-- 2. CLASS_SCHEDULES  (new table)
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS class_schedules (
  id               uuid    PRIMARY KEY DEFAULT gen_random_uuid(),
  service_id       uuid    NOT NULL REFERENCES services(id) ON DELETE CASCADE,
  day_of_week      integer NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
  start_time       text    NOT NULL,   -- "18:00"
  capacity         integer NOT NULL DEFAULT 20,
  practitioner_id  uuid    REFERENCES practitioners(id) ON DELETE SET NULL,
  active           boolean NOT NULL DEFAULT true
);

CREATE INDEX IF NOT EXISTS idx_class_schedules_service   ON class_schedules(service_id);
CREATE INDEX IF NOT EXISTS idx_class_schedules_day       ON class_schedules(day_of_week);
CREATE INDEX IF NOT EXISTS idx_class_schedules_pract     ON class_schedules(practitioner_id);


-- ══════════════════════════════════════════════════════════════════════════════
-- 3. PRACTITIONERS  (table already exists — no structural changes needed)
--    Existing columns (id, name, role, color, photo_url, active, display_order)
--    already satisfy the required fields (id + name).
-- ══════════════════════════════════════════════════════════════════════════════

-- No changes required.


-- ══════════════════════════════════════════════════════════════════════════════
-- 4. BOOKINGS  (table already exists — add missing columns only)
-- ══════════════════════════════════════════════════════════════════════════════

ALTER TABLE bookings
  ADD COLUMN IF NOT EXISTS class_schedule_id uuid REFERENCES class_schedules(id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS client_phone      text;

CREATE INDEX IF NOT EXISTS idx_bookings_class_schedule ON bookings(class_schedule_id);


-- ══════════════════════════════════════════════════════════════════════════════
-- 5. ROW-LEVEL SECURITY
--    Allow the anon key (used by the public booking page) to read services,
--    class_schedules, and practitioners, and to INSERT bookings.
-- ══════════════════════════════════════════════════════════════════════════════

-- services
ALTER TABLE services ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "public read services" ON services;
CREATE POLICY "public read services"
  ON services FOR SELECT
  USING (active = true);

-- class_schedules
ALTER TABLE class_schedules ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "public read class_schedules" ON class_schedules;
CREATE POLICY "public read class_schedules"
  ON class_schedules FOR SELECT
  USING (active = true);

-- practitioners
ALTER TABLE practitioners ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "public read practitioners" ON practitioners;
CREATE POLICY "public read practitioners"
  ON practitioners FOR SELECT
  USING (true);

-- bookings — anon can insert (public booking form) but not read others' bookings
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "public insert bookings" ON bookings;
CREATE POLICY "public insert bookings"
  ON bookings FOR INSERT
  WITH CHECK (true);


-- ══════════════════════════════════════════════════════════════════════════════
-- 6. SEED — starter services
--    Add a small set of real services so the booking page has something to show.
--    Edit names, prices and display_order freely in the Supabase Table Editor.
-- ══════════════════════════════════════════════════════════════════════════════

INSERT INTO services (name, category, "group", color, duration_minutes, price_cents, billing, allow_trial, enquiry, desc, active, display_order)
VALUES
  -- Combat
  ('MMA Class',            'combat', 'Drop-In Classes', '#C9A84C', 60,  0,     'session', true,  false, 'Full MMA striking and grappling session.',          true, 1),
  ('BJJ Class',            'combat', 'Drop-In Classes', '#C9A84C', 60,  0,     'session', true,  false, 'Gi and no-gi Brazilian Jiu-Jitsu.',                 true, 2),
  ('Kickboxing Class',     'combat', 'Drop-In Classes', '#C9A84C', 60,  0,     'session', true,  false, 'Stand-up striking with cardio conditioning.',       true, 3),
  ('Boxing Fitness Class', 'combat', 'Drop-In Classes', '#C9A84C', 60,  0,     'session', true,  false, 'Technical boxing and full-body conditioning.',      true, 4),
  -- Strength
  ('Powerlifting Session', 'strength','Drop-In Classes', '#A88C3C', 60,  0,     'session', true,  false, 'Squat, bench and deadlift coaching.',               true, 1),
  -- PT
  ('Personal Training',    'pt',     '1-on-1',          '#8CA84C', 60,  50000, 'session', false, false, 'Fully personalised 1-on-1 coaching session.',       true, 1),
  -- Recovery
  ('Contrast Therapy',     'recovery','Contrast',        '#4CC9C9', 45,  27000, 'session', false, false, 'Infrared sauna followed by cold plunge.',           true, 1),
  ('Infrared Sauna',       'recovery','Sauna',           '#C9884C', 30,  15000, 'session', false, false, 'Deep infrared heat — solo session.',                true, 2),
  ('Cold Plunge',          'recovery','Cold Plunge',     '#4C8CC9', 20,  8000,  'session', false, false, 'Controlled cold-water immersion.',                  true, 3),
  -- Appointments
  ('Physio Consultation',  'appointment','Physio',       '#C94C4C', 60,  80000, 'session', false, false, 'Injury assessment and rehabilitation planning.',    true, 1),
  ('General Assessment',   'appointment','Assessment',   '#9C4CC9', 45,  50000, 'session', false, false, 'Fitness and health goal-setting session.',          true, 2),
  -- Wellness
  ('Wellness IV Drip',     'appointment','IV Therapy',   '#4CC984', 45,  35000, 'session', false, false, 'Vitamin and mineral infusion.',                     true, 3),
  ('Slimming Programme',   'appointment','Slimming',     '#C94C84', 60,  50000, 'session', false, true,  'Body composition and aesthetic programme.',         true, 4),
  ('Peptide Therapy',      'appointment','Performance',  '#4C84C9', 30,  0,     'session', false, true,  'Medical peptide protocol — consultation required.', true, 5)
ON CONFLICT DO NOTHING;


-- ══════════════════════════════════════════════════════════════════════════════
-- Done. Verify with:
--   SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
-- ══════════════════════════════════════════════════════════════════════════════
