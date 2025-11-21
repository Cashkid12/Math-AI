@echo off
echo Building Equai AI Frontend...
cd frontend
npm run build
echo Frontend build complete!
echo The build files are now in the backend/static directory.
echo You can now deploy the backend which will serve the frontend.
pause