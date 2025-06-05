#!/bin/sh

# Start File Browser first to initialize the database
/filebrowser &
PID=$!

# Wait for it to start
sleep 5

# Now set the branding configuration
/filebrowser config set --branding.name "JCORE" --branding.files "/branding"

# Kill the temporary instance
kill $PID

# Start File Browser normally
exec /filebrowser
