# 🌐 Deployment Guide - ASRI-PyROPS

**Quick guide to deploy the Streamlit app for your team**

---

## ✅ Your GitHub Repository is Ready!

**URL**: https://github.com/anbanpillay/ASRI-PyROPS

All code is pushed and ready to deploy!

---

## 🚀 Deploy to Streamlit Cloud (Recommended - Free!)

### Step 1: Go to Streamlit Cloud

Visit: **https://share.streamlit.io/**

### Step 2: Sign In

- Click **"Sign in"**
- Use your **GitHub account** (anbanpillay)
- Authorize Streamlit to access your repositories

### Step 3: Create New App

1. Click **"New app"** button
2. Fill in the form:

```
Repository: anbanpillay/ASRI-PyROPS
Branch: main
Main file path: rocketpy_migration/src/streamlit_app.py
```

3. **App URL** (optional):
   - Custom subdomain: `asri-pyrops` (or whatever you want)
   - Result: `https://asri-pyrops.streamlit.app`

4. Click **"Deploy!"**

### Step 4: Wait for Deployment

- Takes 2-5 minutes
- You'll see build logs
- Watch for "Your app is live!"

### Step 5: Share with Engineers!

You'll get a URL like:
```
https://asri-pyrops.streamlit.app
```

or

```
https://anbanpillay-asri-pyrops-XXX.streamlit.app
```

**Copy that URL and share it with your team!**

---

## 📱 What Your Engineers Will See

When they visit the URL:
1. Beautiful web interface (no installation needed!)
2. All the controls in the sidebar
3. Can run simulations immediately
4. See results with interactive plots
5. View launch/landing on Google Maps
6. Download data as CSV

---

## 🔐 Make it Private (Optional)

If you want to restrict access:

### Option 1: Use Streamlit Authentication

Edit the app to add:
```python
import streamlit_authenticator as stauth
# Add password protection
```

### Option 2: Deploy on Your Own Server

See "Advanced Deployment Options" below.

---

## 🎨 Customize (Optional)

### Change Colors

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#YOUR_COLOR"  # Change this
```

### Add Company Logo

Add to `streamlit_app.py`:
```python
st.logo("your_logo.png")
```

---

## 📊 Monitor Usage

Streamlit Cloud provides:
- View count
- Error logs
- Resource usage

Access from the Streamlit Cloud dashboard.

---

## 🔄 Update the App

Whenever you push changes to GitHub:
```bash
git add .
git commit -m "Update feature X"
git push
```

Streamlit Cloud **auto-deploys** within 1-2 minutes!

---

## 🆘 Troubleshooting

### App Won't Deploy

**Check**: Is `requirements.txt` in the root directory?
```bash
ls requirements.txt  # Should exist
```

**Fix**: It's already there! If issues, check Streamlit logs.

### Dependencies Error

**Check**: Are all packages in requirements.txt?
```bash
cat requirements.txt | grep rocketpy  # Should show rocketpy
```

**Fix**: Already included! If needed:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### App is Slow

**Normal**: First run takes 30-60s (installing packages)
**After**: Subsequent runs are fast (<5s)

### Can't Access

**Check**: Is the URL correct?
**Try**: Incognito/private browsing mode
**Share**: Send engineers the full URL

---

## 📞 Get Help

### Streamlit Support
- Docs: https://docs.streamlit.io/
- Forum: https://discuss.streamlit.io/
- Status: https://streamlit.statuspage.io/

### Your Team
- Check GitHub issues
- Review logs in Streamlit Cloud dashboard
- Contact: [Your contact info]

---

## 🌐 Advanced Deployment Options

### Option 2: Deploy on Your Own Server

If you have a Linux server:

```bash
# SSH to your server
ssh user@your-server.com

# Clone repo
git clone https://github.com/anbanpillay/ASRI-PyROPS.git
cd ASRI-PyROPS

# Install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run with systemd (persistent)
sudo nano /etc/systemd/system/rocketpy.service
```

Add:
```ini
[Unit]
Description=RocketPy Streamlit App
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/ASRI-PyROPS
ExecStart=/path/to/.venv/bin/streamlit run rocketpy_migration/src/streamlit_app.py --server.port 8501
Restart=always

[Install]
WantedBy=multi-user.target
```

Start:
```bash
sudo systemctl start rocketpy
sudo systemctl enable rocketpy  # Auto-start on boot
```

### Option 3: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.13
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "rocketpy_migration/src/streamlit_app.py"]
```

Build and run:
```bash
docker build -t asri-pyrops .
docker run -p 8501:8501 asri-pyrops
```

---

## ✨ Next Steps After Deployment

1. **Test the App**
   - Visit the URL
   - Run a simulation
   - Verify all features work
   - Check maps display correctly

2. **Share with Engineers**
   - Send them the URL
   - Show them QUICK_START.md
   - Give a quick demo

3. **Gather Feedback**
   - What features do they want?
   - Any issues?
   - Performance concerns?

4. **Iterate**
   - See FUTURE_ENHANCEMENTS.md for ideas
   - Add requested features
   - Push updates (auto-deploys!)

---

## 🎉 You're Done!

Your rocket simulation is now:
- ✅ On GitHub (version controlled)
- ✅ Deployed to the cloud (or ready to deploy)
- ✅ Accessible to your team
- ✅ Auto-updating from Git
- ✅ Professional and impressive!

**Congratulations!** 🚀

---

**Questions?** Check the documentation or open a GitHub issue!

**Last Updated**: 2025-10-19
