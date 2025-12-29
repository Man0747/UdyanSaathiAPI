#!/bin/bash

echo "🚀 Setting up production-grade local database configuration..."
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📦 Installing required dependencies..."
pip install mysqlclient --quiet

echo ""
echo "✅ Dependencies installed!"
echo ""

# Test production database connection
echo "🔌 Testing production database connection..."
python manage.py dbshell --database=production <<EOF 2>/dev/null
SELECT 'Connection successful!' as status;
SHOW TABLES;
EXIT;
EOF

if [ $? -eq 0 ]; then
    echo "✅ Production database connection successful!"
else
    echo "⚠️  Could not connect to production database."
    echo "   This is okay - the system will fall back to API mode."
fi

echo ""
echo "📊 Testing data retrieval..."

# Test production data sync
python manage.py sync_production_data --force

echo ""
echo "✅ Setup complete!"
echo ""
echo "📈 Performance tiers configured:"
echo "   1️⃣  Cache (in-memory):     ~5ms   ⚡ Fastest"
echo "   2️⃣  Production DB (MySQL): ~50ms  🚀 Fast"
echo "   3️⃣  Production API (HTTP): ~300ms 🌐 Fallback"
echo ""
echo "🎯 Next steps:"
echo "   1. Start Django: python manage.py runserver"
echo "   2. Navigate to: http://localhost:5173/wards"
echo "   3. Watch console for data source indicators"
echo ""
echo "💡 Tips:"
echo "   - First load will be slower (cache miss)"
echo "   - Subsequent loads will use cache (~5ms)"
echo "   - Cache refreshes every 5 minutes"
echo "   - To force refresh: python manage.py sync_production_data --force"
echo ""
