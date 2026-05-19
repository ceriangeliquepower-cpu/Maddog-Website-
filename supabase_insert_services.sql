-- Maddog Performance Institute — Services INSERT
-- Run this in Supabase: Dashboard → SQL Editor → New query → paste → Run
-- This inserts all missing services. Safe to run multiple times (uses ON CONFLICT DO NOTHING).

INSERT INTO services (name, category, price_cents, billing, "group", allow_trial, enquiry, active, display_order, color, desc)
VALUES

-- =====================
-- COMBAT SPORTS — additions to existing records
-- =====================
('BJJ Free Trial',           'combat', 0,      'session', 'Free Trials',  true,  false, true, 51, '#C9A84C', 'Try a BJJ class with no commitment — beginners welcome.'),
('Boxing Fitness Free Trial','combat', 0,      'session', 'Free Trials',  true,  false, true, 52, '#C9A84C', 'Experience a Boxing Fitness class on us.'),
('Kids BJJ Free Trial',      'combat', 0,      'session', 'Kids BJJ',     true,  false, true, 53, '#C9A84C', 'Free trial class for kids aged 5–14.'),
('Kids BJJ Monthly',         'combat', 80000,  'monthly', 'Kids BJJ',     false, false, true, 54, '#C9A84C', 'Monthly Kids BJJ membership.'),
('Kids BJJ Drop-In',         'combat', 15000,  'session', 'Kids BJJ',     false, false, true, 55, '#C9A84C', 'Drop-in class for kids.'),

-- =====================
-- STRENGTH & POWERLIFTING
-- =====================
('Powerlifting Drop-In',     'strength', 65000, 'session', 'Drop-In',      false, false, true, 60, '#C9A84C', 'Single drop-in session in the powerlifting gym.'),
('Powerlifting Monthly',     'strength', 0,     'monthly', 'Memberships',  false, true,  true, 61, '#C9A84C', 'Monthly powerlifting membership — enquire for current pricing.'),
('Strength Coaching',        'strength', 0,     'session', 'Coaching',     false, true,  true, 62, '#C9A84C', 'Personalised strength coaching — enquire for packages.'),

-- =====================
-- PERSONAL TRAINING — additions
-- =====================
('Elite PT — 1× per Week',            'pt', 80000,  'monthly', 'Elite Personal Training',  false, false, true, 70, '#C9A84C', 'One elite PT session per week.'),
('Couples PT',                         'pt', 0,      'monthly', 'Couples & Semi-Private',   false, true,  true, 75, '#C9A84C', 'Train together — couples PT packages available on enquiry.'),
('Semi-Private PT (2–4 people)',       'pt', 0,      'monthly', 'Couples & Semi-Private',   false, true,  true, 76, '#C9A84C', 'Small group personal training — enquire for pricing.'),
('Hybrid Performance Coaching',        'pt', 0,      'monthly', 'Hybrid',                   false, true,  true, 77, '#C9A84C', 'Online + in-gym hybrid coaching programme.'),
('PT Free Trial Session',              'pt', 0,      'session', 'Free Trials',              true,  false, true, 78, '#C9A84C', 'One complimentary PT session to experience the Maddog method.'),

-- =====================
-- RECOVERY — IV DRIP THERAPY
-- =====================
('Hydration IV',              'recovery', 60000,  'session', 'IV Drip Therapy', false, false, true, 80, '#68D391', 'Rapid rehydration with electrolytes and vitamins.'),
('Immunity Boost IV',         'recovery', 110000, 'session', 'IV Drip Therapy', false, false, true, 81, '#68D391', 'High-dose Vitamin C and zinc to support immune function.'),
('Recovery IV',               'recovery', 130000, 'session', 'IV Drip Therapy', false, false, true, 82, '#68D391', 'Post-training muscle repair and inflammation reduction.'),
('Anti-Inflammation IV',      'recovery', 130000, 'session', 'IV Drip Therapy', false, false, true, 83, '#68D391', 'Targeted anti-inflammatory protocol for recovery and pain relief.'),
('Myers Cocktail IV',         'recovery', 130000, 'session', 'IV Drip Therapy', false, false, true, 84, '#68D391', 'Classic multi-vitamin and mineral infusion for energy and wellness.'),
('Energy Performance IV',     'recovery', 140000, 'session', 'IV Drip Therapy', false, false, true, 85, '#68D391', 'Pre-competition energy and endurance formula.'),
('Detox IV',                  'recovery', 130000, 'session', 'IV Drip Therapy', false, false, true, 86, '#68D391', 'Liver support and detoxification protocol.'),
('IV Add-On: Glutathione Push',      'recovery', 65000,  'session', 'IV Add-Ons', false, false, true, 87, '#68D391', 'Powerful antioxidant push added to any IV protocol.'),
('IV Add-On: Customised Protocol',   'recovery', 70000,  'session', 'IV Add-Ons', false, false, true, 88, '#68D391', 'Personalised supplement additions based on your bloodwork.'),

-- =====================
-- RECOVERY — AESTHETIC & WELLNESS IV
-- =====================
('Glutathione Glow IV',       'recovery', 120000, 'session', 'Aesthetic & Wellness IV', false, false, true, 90, '#68D391', 'Skin brightening and antioxidant infusion.'),
('NAD+ IV',                   'recovery', 130000, 'session', 'Aesthetic & Wellness IV', false, false, true, 91, '#68D391', 'Cellular regeneration and anti-ageing NAD+ infusion.'),
('Cognitive Enhancement IV',  'recovery', 190000, 'session', 'Aesthetic & Wellness IV', false, false, true, 92, '#68D391', 'Nootropic IV for focus, memory and mental clarity.'),
('Bespoke IV Protocol',       'recovery', 100000, 'session', 'Aesthetic & Wellness IV', false, false, true, 93, '#68D391', 'Custom formulated protocol designed around your goals.'),

-- =====================
-- RECOVERY — CONTRAST THERAPY
-- =====================
('Contrast Therapy — Post-Training (Single)',  'recovery', 8000,  'session', 'Contrast Therapy', false, false, true, 100, '#68D391', 'Single post-training contrast session in shared space.'),
('Contrast Therapy — Post-Training (3-Pack)',  'recovery', 17000, 'session', 'Contrast Therapy', false, false, true, 101, '#68D391', '3-session post-training contrast bundle.'),
('Contrast Therapy — Post-Training (5-Pack)',  'recovery', 25000, 'session', 'Contrast Therapy', false, false, true, 102, '#68D391', '5-session post-training contrast bundle.'),
('Contrast Therapy — General (Single)',        'recovery', 27000, 'session', 'Contrast Therapy', false, false, true, 103, '#68D391', 'Single general contrast therapy session.'),
('Contrast Therapy — General (3-Pack)',        'recovery', 35000, 'session', 'Contrast Therapy', false, false, true, 104, '#68D391', '3-session general contrast therapy bundle.'),

-- =====================
-- RECOVERY — PACKAGES
-- =====================
('Recovery Package — Basic',  'recovery', 90000,  'monthly', 'Recovery Packages', false, false, true, 110, '#68D391', 'Unlimited sauna and ice sessions — shared space.'),
('Recovery Package — Elite',  'recovery', 300000, 'monthly', 'Recovery Packages', false, false, true, 111, '#68D391', 'Private VVIP access — unlimited contrast therapy in private suite.'),

-- =====================
-- RECOVERY — SLIMMING CLINIC
-- =====================
('Slimming Doctor Assessment',        'recovery', 95000, 'session', 'Slimming Clinic', false, false, true, 120, '#68D391', 'Full medical assessment with Dr Du Plessis.'),
('Slimming Protocol Consultation',    'recovery', 50000, 'session', 'Slimming Clinic', false, false, true, 121, '#68D391', 'Personalised slimming protocol consultation.'),

-- =====================
-- RECOVERY — PEPTIDE PROTOCOLS
-- =====================
('Peptide Therapy',           'recovery', 0, 'session', 'Peptide Protocols', false, true, true, 130, '#68D391', 'Performance and recovery peptide protocols — enquire for personalised plan.'),

-- =====================
-- APPOINTMENTS
-- =====================
('Physiotherapy Consultation',       'appointment', 0, 'session', 'Medical Suite',      false, true, true, 140, '#C9A84C', 'Sports physiotherapy assessment and treatment.'),
('Doctor Consultation',              'appointment', 0, 'session', 'Medical Suite',      false, true, true, 141, '#C9A84C', 'Medical consultation with Dr Du Plessis.'),
('Nurse Consultation',               'appointment', 0, 'session', 'Medical Suite',      false, true, true, 142, '#C9A84C', 'Consultation with Sister Amanda Wren Kobus.'),
('InBody Composition Assessment',    'appointment', 0, 'session', 'InBody',             false, true, true, 150, '#C9A84C', 'Full body composition scan and report.'),
('InBody + PT Consult',              'appointment', 0, 'session', 'InBody',             false, true, true, 151, '#C9A84C', 'Body scan paired with a personalised training consultation.'),
('Corporate Wellness Package',       'appointment', 0, 'session', 'Corporate Wellness', false, true, true, 160, '#C9A84C', 'Team wellness programmes — contact us for a quote.')

ON CONFLICT DO NOTHING;

-- Verify insert count
SELECT category, COUNT(*) as total, COUNT(*) FILTER (WHERE active = true) as active
FROM services
GROUP BY category
ORDER BY category;
