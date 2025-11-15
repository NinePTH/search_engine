# 🚀 Python Vector API - Deployment Summary

## ✅ Files Created for Deployment

| File | Purpose | Status |
|------|---------|--------|
| `Dockerfile` | Container image for production | ✅ Ready |
| `docker-compose.yml` | Local development setup | ✅ Ready |
| `render.yaml` | Render.com configuration | ✅ Ready |
| `.dockerignore` | Exclude unnecessary files | ✅ Ready |
| `deploy-render.sh` | Auto-deploy script for Render | ✅ Ready |
| `deploy-railway.sh` | Auto-deploy script for Railway | ✅ Ready |
| `DEPLOYMENT_GUIDE.md` | Full deployment guide | ✅ Ready |
| `QUICK_DEPLOY.md` | Quick start guide | ✅ Ready |

---

## 🌟 Recommended Platform: Render.com

### Why Render?
- ✅ **100% Free** (750 hours/month)
- ✅ **Easiest Setup** (GUI-based, no CLI)
- ✅ **Auto-Deploy** from GitHub
- ✅ **SSL Certificate** included
- ✅ **Custom Domain** support (free)
- ⚠️ Cold start after 15 min (acceptable for free tier)

### How to Deploy (5 Steps)

#### 1. Push Code to GitHub
```bash
cd python-vector-api

# If not already in git
git init
git add .
git commit -m "feat: Python Vector API with NLP search"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/python-vector-api.git
git push -u origin main
```

#### 2. Go to Render.com
- Visit: https://render.com
- Sign up with GitHub
- Click "New +" → "Web Service"

#### 3. Connect Repository
- Select: `python-vector-api` repository
- Branch: `main`

#### 4. Configure Service
```yaml
Name: fitrecipes-vector-api
Environment: Docker
Region: Singapore (closest to Thailand)
Branch: main
Instance Type: Free
```

#### 5. Add Environment Variables
```bash
DATABASE_URL=postgresql://xxx@xxx.supabase.co:5432/postgres?sslmode=require
PYTHON_API_KEY=vsk_aB3dE5fG7hI9jK1lM3nO5pQ7rS9tU1vW3xY5zA7bC9dE1fG3hI5jK7lM9
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...
ENVIRONMENT=production
LOG_LEVEL=INFO
```

#### 6. Deploy!
- Click "Create Web Service"
- Wait 5-10 minutes (first deployment)
- Your API: `https://fitrecipes-vector-api.onrender.com`

---

## 🧪 Test Your Deployed API

### Test 1: Health Check
```bash
curl https://fitrecipes-vector-api.onrender.com/health
```

Expected:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "database_connected": true
}
```

### Test 2: Smart Search
```bash
curl -X POST https://fitrecipes-vector-api.onrender.com/search/smart \
  -H "Content-Type: application/json" \
  -H "X-API-Key: vsk_aB3dE5fG7hI9jK1lM3nO5pQ7rS9tU1vW3xY5zA7bC9dE1fG3hI5jK7lM9" \
  -d '{
    "query": "quick vegan breakfast",
    "limit": 3
  }'
```

### Test 3: Ingredient Search
```bash
curl -X POST https://fitrecipes-vector-api.onrender.com/search/ingredients \
  -H "Content-Type: application/json" \
  -H "X-API-Key: vsk_aB3dE5fG7hI9jK1lM3nO5pQ7rS9tU1vW3xY5zA7bC9dE1fG3hI5jK7lM9" \
  -d '{
    "ingredients": ["chicken", "garlic"],
    "match_mode": "any",
    "limit": 3
  }'
```

---

## 🔧 Update Backend (Hono.js) Configuration

### Step 1: Update .env
```bash
# Development (local Python API)
PYTHON_API_URL=http://localhost:8000

# Production (Render deployment)
PYTHON_API_URL=https://fitrecipes-vector-api.onrender.com

# API Key (same for both)
PYTHON_API_KEY=vsk_aB3dE5fG7hI9jK1lM3nO5pQ7rS9tU1vW3xY5zA7bC9dE1fG3hI5jK7lM9
```

### Step 2: Test Connection from Backend
```typescript
// src/test-python-api.ts
import { checkVectorApiHealth, searchRecipesSmart } from './utils/vectorApi';

async function testPythonApi() {
  try {
    // Test health
    const health = await checkVectorApiHealth();
    console.log('✅ Python API Health:', health);

    // Test search
    const results = await searchRecipesSmart('quick vegan breakfast', 3);
    console.log('✅ Search Results:', results.total, 'recipes found');
  } catch (error) {
    console.error('❌ Error:', error);
  }
}

testPythonApi();
```

Run test:
```bash
bun run src/test-python-api.ts
```

---

## 📊 Platform Comparison

| Feature | Render.com | Railway.app | Fly.io | Heroku |
|---------|------------|-------------|--------|--------|
| **Free Tier** | ✅ 750h/mo | ✅ $5/mo credit | ✅ 3 VMs | ❌ Paid only |
| **RAM** | 512MB | 512MB | 256MB | N/A |
| **Cold Start** | 30-50s | ❌ None | ❌ None | N/A |
| **Setup Difficulty** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Auto Deploy** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Custom Domain** | ✅ Free | ✅ Free | ✅ Free | 💰 Paid |
| **SSL** | ✅ Free | ✅ Free | ✅ Free | ✅ Free |
| **Logs** | ✅ Good | ✅ Excellent | ✅ Good | ✅ Good |
| **Best For** | Beginners | Performance | Advanced | Enterprise |

**Winner**: 🏆 **Render.com** - Best balance of ease and features

---

## 🚨 Common Issues & Solutions

### Issue 1: Build Failed (Out of Memory)
**Solution**: Use CPU-only PyTorch
```dockerfile
# In Dockerfile, change:
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
```

### Issue 2: Cold Start Too Slow
**Solutions**:
1. Keep-alive service (free): https://cron-job.org
   - Ping `/health` every 10 minutes
2. Upgrade to paid tier ($7/mo - no cold start)

### Issue 3: Database Connection Failed
**Solution**: Check SSL mode in DATABASE_URL
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
```

### Issue 4: Model Download Failed
**Solution**: NLTK data downloads automatically in Dockerfile
```dockerfile
RUN python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
```

---

## 📈 Cost Estimate

### Free Tier (Render.com)
- **Cost**: $0/month
- **Limitations**: 
  - Cold start after 15 min inactivity
  - 512MB RAM
  - 0.1 CPU
- **Suitable for**: Development, staging, small production

### Paid Tier (Render.com)
- **Cost**: $7/month
- **Benefits**:
  - No cold start
  - 512MB RAM
  - Always-on
  - Better performance
- **Suitable for**: Production with consistent traffic

### Railway.app
- **Cost**: $5-10/month (usage-based)
- **Benefits**:
  - No cold start
  - Better performance than Render free
  - Excellent logs
- **Suitable for**: Production

---

## ✅ Deployment Checklist

- [ ] All files created (Dockerfile, render.yaml, etc.)
- [ ] Code pushed to GitHub
- [ ] Render.com account created
- [ ] Web Service created and configured
- [ ] Environment variables added
- [ ] Deployment successful (check logs)
- [ ] Health check passes
- [ ] Backend .env updated with deployed URL
- [ ] Integration test from backend successful
- [ ] Search endpoints tested
- [ ] Monitoring set up (optional)

---

## 🎯 Next Steps

1. **Now**: Deploy to Render.com using steps above
2. **Test**: Verify all endpoints work
3. **Integrate**: Update backend to use deployed URL
4. **Monitor**: Check Render dashboard for logs
5. **Optimize**: Consider paid tier if cold start is issue
6. **Scale**: Add caching (Redis) if needed

---

## 🆘 Need Help?

- **Full Guide**: See `DEPLOYMENT_GUIDE.md`
- **Quick Start**: See `QUICK_DEPLOY.md`
- **Integration**: See `docs/PYTHON_VECTOR_API_INTEGRATION.md`
- **Examples**: See `docs/BACKEND_INTEGRATION_EXAMPLES.md`

**Deploy Scripts**:
- Render: `./deploy-render.sh`
- Railway: `./deploy-railway.sh`

---

## 🎉 Summary

You now have:
- ✅ Production-ready Dockerfile
- ✅ Deployment configs for 3 platforms
- ✅ Auto-deploy scripts
- ✅ Full documentation
- ✅ Integration examples

**Time to deploy**: 10-15 minutes
**Cost**: $0 (free tier)

**Recommended Flow**:
1. Deploy to Render (free) → Test
2. If satisfied → Keep free tier
3. If need better performance → Upgrade ($7/mo) or use Railway

Good luck! 🚀
# search_engine
