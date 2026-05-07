import { createClient } from '@supabase/supabase-js'

const SUPABASE_URL = 'https://rptsefqjbwlocebywgpw.supabase.co'
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJwdHNlZnFqYndsb2NlYnl3Z3B3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc2MzEwMTgsImV4cCI6MjA5MzIwNzAxOH0.5FYLXothbSXMfGXNVNTbgWL1HafZIt2V3EliC94pEhY'

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)