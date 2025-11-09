# Quick Start Checklist - Windows Server

Follow this checklist to get CloudDrive2 Media Streaming up and running on Windows Server.

## Prerequisites Checklist

- [ ] Windows Server 2012 R2 or later (or Windows 10/11)
- [ ] Administrator access to the server
- [ ] Python 3.8+ installed and in PATH
- [ ] CloudDrive2 installed and configured (optional for testing)
- [ ] Internet connection for downloading dependencies

## Installation Steps

### Step 1: Download Application
- [ ] Clone or download the repository to `C:\lynx` (or preferred location)
- [ ] Open Command Prompt as Administrator
- [ ] Navigate to application directory: `cd C:\lynx`

### Step 2: Install Dependencies
- [ ] Run: `install.bat`
- [ ] Wait for all dependencies to install successfully
- [ ] Verify no errors were displayed

### Step 3: Configure Application
- [ ] Run: `setup.bat`
- [ ] Enter CloudDrive2 mount path (e.g., `C:\CloudDrive2`)
- [ ] Choose port number (default: 8000)
- [ ] Enable authentication (recommended)
- [ ] Set username and password if authentication enabled
- [ ] Verify `.env` file was created

### Step 4: Test Installation
- [ ] Run: `test_system.bat`
- [ ] Review test results
- [ ] Fix any failed tests before proceeding

### Step 5: Configure Firewall
- [ ] Run: `configure_firewall.bat`
- [ ] Choose appropriate firewall rule type
- [ ] Verify rule was created successfully

### Step 6: Test Manual Start
- [ ] Run: `start.bat`
- [ ] Wait for server to start
- [ ] Open browser to `http://localhost:8000`
- [ ] Verify web interface loads
- [ ] Test API: `http://localhost:8000/docs`
- [ ] Stop server with Ctrl+C

### Step 7: Install as Windows Service (Optional)
- [ ] Run: `install_service.bat` (as Administrator)
- [ ] Choose to start service now
- [ ] Verify service is running: `sc query CloudDrive2Streaming`
- [ ] Test access again: `http://localhost:8000`

## Post-Installation Verification

### Verify File Access
- [ ] Navigate to `http://localhost:8000/api/files/list`
- [ ] Verify files from CloudDrive2 are listed
- [ ] Click on a file to test streaming

### Verify Authentication (if enabled)
- [ ] Try accessing without credentials (should fail)
- [ ] Login with configured username/password
- [ ] Verify access is granted

### Verify Range Requests
- [ ] Open a video file in browser
- [ ] Verify seeking/skipping works
- [ ] Test download resume functionality

### Network Access (if needed)
- [ ] Test access from another machine on network
- [ ] URL: `http://server-ip:8000`
- [ ] Verify firewall rule allows access

## Configuration Checklist

### Security Configuration
- [ ] Changed `SECRET_KEY` to random value
- [ ] Set strong `AUTH_PASSWORD`
- [ ] Configured `CORS_ORIGINS` to trusted domains
- [ ] Set `DEBUG=False` for production
- [ ] Reviewed and applied security best practices

### Performance Configuration
- [ ] Set `MAX_WORKERS` based on CPU cores
- [ ] Configured `CHUNK_SIZE` appropriately
- [ ] Enabled caching (`CACHE_ENABLED=True`)
- [ ] Adjusted `CACHE_TTL` and `CACHE_MAX_SIZE`

### Integration Configuration (if using Discuz)
- [ ] Reviewed `examples/discuz/README.md`
- [ ] Copied integration files to Discuz directory
- [ ] Updated streaming server URL in PHP
- [ ] Tested authentication from Discuz
- [ ] Verified file streaming works

## Troubleshooting Checklist

If something doesn't work:

### Application Won't Start
- [ ] Check Python is installed: `python --version`
- [ ] Check dependencies: run `install.bat` again
- [ ] Review logs in `logs\app.log`
- [ ] Verify port is not in use: `netstat -ano | findstr :8000`

### Service Won't Start
- [ ] Check service status: `sc query CloudDrive2Streaming`
- [ ] Review service logs in `logs\service_error.log`
- [ ] Check Event Viewer (Windows Logs → Application)
- [ ] Try manual start first: `start.bat`

### Can't Access from Network
- [ ] Verify firewall rule: `netsh advfirewall firewall show rule name="CloudDrive2 Streaming"`
- [ ] Check `HOST=0.0.0.0` in `.env`
- [ ] Test connectivity: `ping server-ip`
- [ ] Test port: `telnet server-ip 8000`

### Files Not Found
- [ ] Verify CloudDrive2 is running
- [ ] Check mount path in `.env`
- [ ] Verify path permissions
- [ ] Test path exists: `dir C:\CloudDrive2`

### Authentication Issues
- [ ] Verify credentials in `.env`
- [ ] Test with curl: `curl -u username:password http://localhost:8000/api/auth/token`
- [ ] Check for typos in username/password
- [ ] Try disabling auth temporarily to test

## Maintenance Checklist

### Daily
- [ ] Monitor service status
- [ ] Check for errors in logs

### Weekly
- [ ] Review log files size
- [ ] Check disk space
- [ ] Monitor performance

### Monthly
- [ ] Update Python dependencies
- [ ] Review security logs
- [ ] Test backup procedures
- [ ] Verify SSL certificate (if using HTTPS)

## Support Resources

- Windows Setup Guide: `WINDOWS_README.md`
- Windows Service Guide: `WINDOWS_SERVICE_GUIDE.md`
- API Documentation: `API.md` or `http://localhost:8000/docs`
- Discuz Integration: `examples/discuz/README.md`
- GitHub Issues: https://github.com/lyjlyjn/lynx/issues

## Next Steps

After completing this checklist:

1. **Documentation**: Bookmark important URLs and documentation
2. **Monitoring**: Set up monitoring and alerting
3. **Backups**: Configure automated backups of `.env` and config
4. **SSL**: Configure SSL/TLS for production use
5. **Integrate**: Integrate with Discuz or other applications
6. **Scale**: Consider load balancing for high traffic

## Success Criteria

Your installation is successful when:

- ✅ Service is running and accessible
- ✅ Authentication works correctly
- ✅ Files can be listed and streamed
- ✅ Range requests work (seeking in videos)
- ✅ Network access configured properly
- ✅ Firewall rules in place
- ✅ Logs are being written
- ✅ All tests pass

Congratulations! Your CloudDrive2 Media Streaming application is ready for use! 🎉
